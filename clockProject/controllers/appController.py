"""Application controller that wires services and UI."""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDialog, QMessageBox

from models.alarm import Alarm
from models.clockSettings import ClockSettings
from services.alarmService import AlarmService
from services.animationService import AnimationService
from services.clockService import ClockService
# Countdown timer removed from active UI per requirements
from services.historyService import HistoryService
from services.pomodoroService import PomodoroService
from services.stopwatchService import StopwatchService
from services.themeService import ThemeService
from services.timezoneService import TimezoneService
from ui.dialogs.alarmDialog import AlarmDialog
from ui.mainWindow import MainWindow


class AppController:
    """Coordinates services and user interface interactions."""

    def __init__(self) -> None:
        self.settings = ClockSettings()

        self.alarmService = AlarmService()
        self.stopwatchService = StopwatchService()
        # countdownService intentionally not instantiated (Temporizador removed)
        self.pomodoroService = PomodoroService()
        self.timezoneService = TimezoneService(self.settings.selectedTimezoneCode)
        self.clockService = ClockService(self.settings, self.timezoneService)
        self.themeService = ThemeService()
        self.historyService = HistoryService()
        self.animationService = AnimationService()

        self.mainWindow = MainWindow()
        self.clockTimer = QTimer(self.mainWindow)
        self.clockTimer.setInterval(1000)
        self.stopwatchTimer = QTimer(self.mainWindow)
        self.stopwatchTimer.setInterval(100)
        self.pomodoroTimer = QTimer(self.mainWindow)
        self.pomodoroTimer.setInterval(1000)

        self._connectSignals()
        self.updateClock()
        self.clockTimer.start()
        # timers run while active
        self.stopwatchTimer.timeout.connect(self._onStopwatchTick)
        self.pomodoroTimer.timeout.connect(self._onPomodoroTick)
        # ensure analog widget mode matches initial selected tab
        self._onTabChanged(self.mainWindow.tabs.currentIndex())

    def _connectSignals(self) -> None:
        """Connect UI signals to controller handlers."""
        self.clockTimer.timeout.connect(self.updateClock)
        self.mainWindow.openClockButton.clicked.connect(self.mainWindow.showClockPage)
        self.mainWindow.previewAnalogClockWidget.clicked.connect(self.mainWindow.showClockPage)
        self.mainWindow.backButton.clicked.connect(self.mainWindow.showHomePage)

        if "Pomodoro" in self.mainWindow.homeCards:
            self.mainWindow.homeCards["Pomodoro"].clicked.connect(lambda: self.mainWindow.navigateToTab(0))
        if "Alarmas" in self.mainWindow.homeCards:
            self.mainWindow.homeCards["Alarmas"].clicked.connect(lambda: self.mainWindow.navigateToTab(1))
        if "Cronómetro" in self.mainWindow.homeCards:
            self.mainWindow.homeCards["Cronómetro"].clicked.connect(lambda: self.mainWindow.navigateToTab(2))
        if "Zona horaria" in self.mainWindow.homeCards:
            self.mainWindow.homeCards["Zona horaria"].clicked.connect(lambda: self.mainWindow.navigateToTab(3))
        if "Configuración" in self.mainWindow.homeCards:
            self.mainWindow.homeCards["Configuración"].clicked.connect(lambda: self.mainWindow.navigateToTab(4))

        self.mainWindow.alarmPanel.addButton.clicked.connect(self.addAlarm)
        self.mainWindow.alarmPanel.editButton.clicked.connect(self.editSelectedAlarm)
        self.mainWindow.alarmPanel.removeButton.clicked.connect(self.removeSelectedAlarm)
        self.mainWindow.alarmPanel.toggleButton.clicked.connect(self.toggleSelectedAlarm)
        self.mainWindow.alarmPanel.previousButton.clicked.connect(self.moveToPreviousAlarm)
        self.mainWindow.alarmPanel.nextButton.clicked.connect(self.moveToNextAlarm)
        self.mainWindow.alarmPanel.alarmListWidget.currentRowChanged.connect(self.onAlarmSelectionChanged)
        # Tab change to switch analog display mode
        self.mainWindow.tabs.currentChanged.connect(self._onTabChanged)

        # Stopwatch controls
        self.mainWindow.stopwatchPanel.startButton.clicked.connect(self._handleStartStopwatch)
        self.mainWindow.stopwatchPanel.pauseButton.clicked.connect(self._handlePauseStopwatch)
        self.mainWindow.stopwatchPanel.resumeButton.clicked.connect(self._handleResumeStopwatch)
        self.mainWindow.stopwatchPanel.resetButton.clicked.connect(self._handleResetStopwatch)
        self.mainWindow.stopwatchPanel.lapButton.clicked.connect(self._handleAddLap)
        self.mainWindow.stopwatchPanel.deleteButton.clicked.connect(self._handleDeleteLap)
        self.mainWindow.stopwatchPanel.previousButton.clicked.connect(self._handlePreviousLap)
        self.mainWindow.stopwatchPanel.nextButton.clicked.connect(self._handleNextLap)

        self.mainWindow.timezonePanel.previousButton.clicked.connect(self._handlePreviousTimezone)
        self.mainWindow.timezonePanel.nextButton.clicked.connect(self._handleNextTimezone)

        # Pomodoro controls
        self.mainWindow.pomodoroPanel.toggleButton.clicked.connect(self._handlePomodoroToggle)
        self.mainWindow.pomodoroPanel.skipButton.clicked.connect(self._handlePomodoroSkip)
        self.mainWindow.pomodoroPanel.resetButton.clicked.connect(self._handlePomodoroReset)
        self.mainWindow.pomodoroPanel.settingsChanged.connect(self._handlePomodoroSettingsChanged)

        # Settings controls
        self.mainWindow.settingsPanel.settingsChanged.connect(self._handleApplySettings)

        self.refreshPomodoroPanel()
        self.refreshAlarmPanel()
        self.refreshTimezonePanel()
        self._initializeSettingsPanel()

    def refreshAlarmPanel(self, selectedAlarmId: int | None = None) -> None:
        """Refresh the alarm panel using the service state."""
        alarms = self.alarmService.getAllAlarms()
        self.mainWindow.alarmPanel.setAlarms(alarms, selectedAlarmId)

        if selectedAlarmId is not None:
            self.alarmService.getCurrentAlarm()

    def refreshTimezonePanel(self) -> None:
        """Refresh the timezone panel using the current service state."""
        currentTimezone = self.timezoneService.getCurrentTimezone()
        if currentTimezone is None:
            return

        currentDateTime = self.clockService.getCurrentDateTime()
        self.mainWindow.timezonePanel.updateTimezoneInfo(
            currentTimezone.cityName,
            currentTimezone.timezoneCode,
            self.clockService.getCurrentTimeText(currentDateTime),
        )

    # ---------------------
    # Stopwatch helpers
    # ---------------------
    def refreshStopwatchPanel(
        self,
        selectedLapNumber: int | None = None,
        refreshLapList: bool = True,
    ) -> None:
        """Refresh stopwatch text and optionally lap list."""
        # Always keep small digital panel display updated.
        timeText = self.stopwatchService.getFormattedElapsedTime()
        self.mainWindow.stopwatchPanel.smallTimeLabel.setText(timeText)

        if not refreshLapList:
            return

        laps = self.stopwatchService.getAllLaps()
        lapListWidget = self.mainWindow.stopwatchPanel.lapListWidget
        lapListWidget.clear()
        if not laps:
            lapListWidget.addItem("Sin vueltas registradas")
            return

        selectedIndex = None
        for index, lap in enumerate(laps):
            lapListWidget.addItem(f"V{lap.lapNumber}  {lap.formattedElapsedTime}  ({lap.timestampText})")
            if selectedLapNumber is not None and lap.lapNumber == selectedLapNumber:
                selectedIndex = index

        if selectedIndex is None:
            selectedIndex = len(laps) - 1
        lapListWidget.setCurrentRow(selectedIndex)

    def updateStopwatchButtons(self) -> None:
        """Enable or disable stopwatch buttons based on the current stopwatch state."""
        isRunning = self.stopwatchService.isRunning()
        isPaused = self.stopwatchService.isPaused()
        hasLaps = len(self.stopwatchService.getAllLaps()) > 0
        hasStarted = self.stopwatchService.hasStarted()

        self.mainWindow.stopwatchPanel.startButton.setEnabled(not isRunning)
        self.mainWindow.stopwatchPanel.pauseButton.setEnabled(isRunning and not isPaused)
        self.mainWindow.stopwatchPanel.resumeButton.setEnabled(isRunning and isPaused)
        self.mainWindow.stopwatchPanel.resetButton.setEnabled(hasStarted)
        self.mainWindow.stopwatchPanel.lapButton.setEnabled(isRunning or isPaused)
        self.mainWindow.stopwatchPanel.deleteButton.setEnabled(hasLaps)
        self.mainWindow.stopwatchPanel.previousButton.setEnabled(hasLaps)
        self.mainWindow.stopwatchPanel.nextButton.setEnabled(hasLaps)

    def _applyTimezoneChange(self, timezoneItem) -> None:
        """Update settings and refresh every timezone-dependent display."""
        if timezoneItem is None:
            return

        self.settings.selectedTimezoneCode = timezoneItem.timezoneCode
        self.refreshTimezonePanel()
        self.updateClock()

    def _handleNextTimezone(self) -> None:
        timezoneItem = self.timezoneService.moveNextTimezone()
        self._applyTimezoneChange(timezoneItem)

    def _handlePreviousTimezone(self) -> None:
        timezoneItem = self.timezoneService.movePreviousTimezone()
        self._applyTimezoneChange(timezoneItem)

    def _handleStartStopwatch(self) -> None:
        self.stopwatchService.start()
        self.stopwatchTimer.start()
        self.mainWindow.analogClockWidget.setDisplayMode("stopwatch")
        self.mainWindow.analogClockWidget.updateStopwatchElapsedMilliseconds(0)
        self.refreshStopwatchPanel()
        self.updateStopwatchButtons()

    def _handlePauseStopwatch(self) -> None:
        self.stopwatchService.pause()
        self.stopwatchTimer.stop()
        self.mainWindow.analogClockWidget.updateStopwatchElapsedMilliseconds(
            self.stopwatchService.getElapsedMilliseconds()
        )
        self.refreshStopwatchPanel(refreshLapList=False)
        self.updateStopwatchButtons()

    def _handleResumeStopwatch(self) -> None:
        self.stopwatchService.resume()
        if self.stopwatchService.isRunning() and not self.stopwatchService.isPaused():
            self.stopwatchTimer.start()
        self.refreshStopwatchPanel(refreshLapList=False)
        self.updateStopwatchButtons()

    def _handleResetStopwatch(self) -> None:
        self.stopwatchService.resetTimeOnly()
        self.stopwatchTimer.stop()
        # Force immediate visual reset on analog stopwatch.
        self.mainWindow.analogClockWidget.setDisplayMode("stopwatch")
        self.mainWindow.analogClockWidget.updateStopwatchElapsedMilliseconds(0)
        self.refreshStopwatchPanel()
        self.updateStopwatchButtons()

    def _handleAddLap(self) -> None:
        lap = self.stopwatchService.addLap()
        if lap is None:
            QMessageBox.warning(self.mainWindow, "Aviso", "El cronómetro no está en ejecución.")
            return
        self.refreshStopwatchPanel(selectedLapNumber=lap.lapNumber)
        self.updateStopwatchButtons()

    def _handleDeleteLap(self) -> None:
        """Delete the currently selected lap."""
        laps = self.stopwatchService.getAllLaps()
        if not laps:
            QMessageBox.warning(self.mainWindow, "Aviso", "Selecciona una vuelta para borrar.")
            return

        lapListWidget = self.mainWindow.stopwatchPanel.lapListWidget
        currentRow = lapListWidget.currentRow()
        if currentRow < 0 or currentRow >= len(laps):
            QMessageBox.warning(self.mainWindow, "Aviso", "Selecciona una vuelta para borrar.")
            return

        selectedLap = laps[currentRow]
        success = self.stopwatchService.removeLap(selectedLap.lapNumber)

        if not success:
            return

        remainingLaps = self.stopwatchService.getAllLaps()
        if remainingLaps:
            nextIndex = min(currentRow, len(remainingLaps) - 1)
            self.refreshStopwatchPanel(selectedLapNumber=remainingLaps[nextIndex].lapNumber)
        else:
            self.refreshStopwatchPanel()
        self.updateStopwatchButtons()

    def _handleNextLap(self) -> None:
        moved = self.stopwatchService.moveNextLap()
        if moved is not None:
            self.refreshStopwatchPanel(selectedLapNumber=moved.lapNumber)
        self.updateStopwatchButtons()

    def _handlePreviousLap(self) -> None:
        moved = self.stopwatchService.movePreviousLap()
        if moved is not None:
            self.refreshStopwatchPanel(selectedLapNumber=moved.lapNumber)
        self.updateStopwatchButtons()

    def _onStopwatchTick(self) -> None:
        # Called by stopwatch QTimer to update display while running
        if not self.stopwatchService.isRunning():
            self.stopwatchTimer.stop()
            return
        self.stopwatchService.updateElapsedTime()
        elapsedMilliseconds = self.stopwatchService.getElapsedMilliseconds()
        # update analog widget in stopwatch mode
        self.mainWindow.analogClockWidget.setDisplayMode("stopwatch")
        self.mainWindow.analogClockWidget.updateStopwatchElapsedMilliseconds(elapsedMilliseconds)
        # keep stopwatch panel text fresh continuously (list refresh not needed every tick)
        self.refreshStopwatchPanel(refreshLapList=False)
        self.updateStopwatchButtons()

    def _getSelectedAlarm(self) -> Alarm | None:
        """Return the currently selected alarm if one exists."""
        alarms = self.alarmService.getAllAlarms()
        alarmId = self.mainWindow.alarmPanel.getSelectedAlarmId(alarms)
        if alarmId is None:
            return None
        return self.alarmService.findAlarmById(alarmId)

    def addAlarm(self) -> None:
        """Open the dialog to create a new alarm."""
        dialog = AlarmDialog(self.mainWindow)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.getAlarmData()
        newAlarm = Alarm(
            alarmId=0,
            hour=data["hour"],
            minute=data["minute"],
            label=data["label"],
            enabled=data["enabled"],
        )
        createdAlarm = self.alarmService.addAlarm(newAlarm)
        self.refreshAlarmPanel(createdAlarm.alarmId)

    def editSelectedAlarm(self) -> None:
        """Edit the currently selected alarm."""
        selectedAlarm = self._getSelectedAlarm()
        if selectedAlarm is None:
            return

        dialog = AlarmDialog(
            self.mainWindow,
            alarmData={
                "hour": selectedAlarm.hour,
                "minute": selectedAlarm.minute,
                "label": selectedAlarm.label,
                "enabled": selectedAlarm.enabled,
            },
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.getAlarmData()
        updatedAlarm = Alarm(
            alarmId=selectedAlarm.alarmId,
            hour=data["hour"],
            minute=data["minute"],
            label=data["label"],
            enabled=data["enabled"],
        )
        self.alarmService.updateAlarm(selectedAlarm.alarmId, updatedAlarm)
        self.refreshAlarmPanel(selectedAlarm.alarmId)

    def removeSelectedAlarm(self) -> None:
        """Remove the currently selected alarm."""
        selectedAlarm = self._getSelectedAlarm()
        if selectedAlarm is None:
            return

        self.alarmService.removeAlarm(selectedAlarm.alarmId)
        self.refreshAlarmPanel()

    def toggleSelectedAlarm(self) -> None:
        """Toggle the enabled state of the selected alarm."""
        selectedAlarm = self._getSelectedAlarm()
        if selectedAlarm is None:
            return

        self.alarmService.toggleAlarm(selectedAlarm.alarmId)
        self.refreshAlarmPanel(selectedAlarm.alarmId)

    def moveToNextAlarm(self) -> None:
        """Move the circular selection to the next alarm."""
        movedAlarm = self.alarmService.moveNextAlarm()
        if movedAlarm is None:
            return

        self.refreshAlarmPanel(movedAlarm.alarmId)

    def moveToPreviousAlarm(self) -> None:
        """Move the circular selection to the previous alarm."""
        movedAlarm = self.alarmService.movePreviousAlarm()
        if movedAlarm is None:
            return

        self.refreshAlarmPanel(movedAlarm.alarmId)

    def onAlarmSelectionChanged(self, row: int) -> None:
        """Keep the service cursor aligned with the visible selection."""
        alarms = self.alarmService.getAllAlarms()
        if row < 0 or row >= len(alarms):
            return

        selectedAlarm = alarms[row]
        while self.alarmService.getCurrentAlarm() is not selectedAlarm:
            movedAlarm = self.alarmService.moveNextAlarm()
            if movedAlarm is None or movedAlarm is selectedAlarm:
                break

    def updateClock(self) -> None:
        """Refresh the UI using the current value from the clock service."""
        currentDateTime = self.clockService.getCurrentDateTime()
        self.mainWindow.updateDigitalClock(self.clockService.getCurrentTimeText(currentDateTime))
        self.mainWindow.updateDateLabel(self.clockService.getCurrentDateText(currentDateTime))
        self.mainWindow.updateAnalogClock(currentDateTime)
        self.refreshTimezonePanel()

        triggeredAlarms = self.alarmService.checkTriggeredAlarms(currentDateTime)
        for alarm in triggeredAlarms:
            QMessageBox.information(
                self.mainWindow,
                "Alarma",
                f"Alarma activada: {alarm.getDisplayTime()} - {alarm.label}",
            )

    def _onTabChanged(self, index: int) -> None:
        """Switch the analog widget between clock and stopwatch modes based on selected tab."""
        widget = self.mainWindow.tabs.widget(index)
        if widget is self.mainWindow.stopwatchPanel:
            # switch to stopwatch mode and feed current elapsed time
            self.mainWindow.analogClockWidget.setDisplayMode("stopwatch")
            self.mainWindow.analogClockWidget.updateStopwatchElapsedMilliseconds(self.stopwatchService.getElapsedMilliseconds())
            self.refreshStopwatchPanel(refreshLapList=True)
            self.updateStopwatchButtons()
        elif widget is self.mainWindow.pomodoroPanel:
            self.mainWindow.analogClockWidget.setDisplayMode("pomodoro")
            self.refreshPomodoroPanel()
        else:
            # regular clock mode
            self.mainWindow.analogClockWidget.setDisplayMode("clock")
            self.mainWindow.updateAnalogClock(self.clockService.getCurrentDateTime())

    # ---------------------
    # Pomodoro helpers
    # ---------------------
    def refreshPomodoroPanel(self) -> None:
        """Update Pomodoro UI elements from service state."""
        phase = self.pomodoroService.getCurrentPhase()
        if not phase:
            return

        self.mainWindow.pomodoroPanel.updateDisplay(
            phaseName=phase.name,
            timeText=self.pomodoroService.getFormattedTime(),
            completedCount=self.pomodoroService.completedPomodoros,
            isRunning=self.pomodoroService.isRunning(),
            phaseColor=phase.colorHex
        )

        # also update the analog widget state
        self.mainWindow.analogClockWidget.updatePomodoroState(
            remainingMs=self.pomodoroService.remainingSeconds * 1000,
            totalMs=phase.totalSeconds * 1000,
            colorHex=phase.colorHex
        )

    def _handlePomodoroToggle(self) -> None:
        self.pomodoroService.toggle()
        if self.pomodoroService.isRunning():
            self.pomodoroTimer.start()
        else:
            self.pomodoroTimer.stop()
        self.refreshPomodoroPanel()

    def _handlePomodoroSkip(self) -> None:
        self.pomodoroService.skipPhase()
        self.pomodoroTimer.stop()
        self.refreshPomodoroPanel()

    def _handlePomodoroReset(self) -> None:
        self.pomodoroService.reset()
        self.pomodoroTimer.stop()
        self.refreshPomodoroPanel()

    def _handlePomodoroSettingsChanged(self) -> None:
        focus, shortBreak, longBreak = self.mainWindow.pomodoroPanel.getDurations()
        self.pomodoroService.updatePhaseDurations(focus, shortBreak, longBreak)
        self.refreshPomodoroPanel()

    def _onPomodoroTick(self) -> None:
        phaseCompleted = self.pomodoroService.tick()
        self.refreshPomodoroPanel()
        if phaseCompleted:
            self.pomodoroTimer.stop()
            # Show a message or play a sound
            QMessageBox.information(
                self.mainWindow,
                "Pomodoro",
                f"¡Tiempo terminado! Preparando la siguiente fase: {self.pomodoroService.getCurrentPhase().name}",
            )

    def _initializeSettingsPanel(self) -> None:
        """Load themes, styles, and current settings into the settings panel."""
        themes = self.themeService.getAllThemes()
        styles = self.themeService.getAllClockStyles()

        self.mainWindow.settingsPanel.setThemes(themes)
        self.mainWindow.settingsPanel.setClockStyles(styles)

        self.mainWindow.settingsPanel.setThemeSelection(self.settings.selectedThemeId)
        self.mainWindow.settingsPanel.setClockStyleSelection(self.settings.selectedClockStyleId)
        self.mainWindow.settingsPanel.setShowSeconds(self.settings.showSeconds)
        self.mainWindow.settingsPanel.setShowDateInfo(self.settings.showDateInfo)
        self.mainWindow.settingsPanel.setTimeFormat(self.settings.use24HourFormat)

        # Apply initial theme and style
        self._applyCurrentThemeAndStyle()

    def _applyCurrentThemeAndStyle(self) -> None:
        """Apply the current theme and clock style to the UI."""
        theme = self.themeService.getThemeById(self.settings.selectedThemeId)
        if theme:
            styleSheet = self.themeService.applyTheme(theme)
            self.mainWindow.setStyleSheet(styleSheet)

        style = self.themeService.getClockStyleById(self.settings.selectedClockStyleId)
        if style:
            # Inject dynamic settings into the style before passing it to the clock
            style.showSeconds = self.settings.showSeconds
            style.showDateInfo = self.settings.showDateInfo
            
            self.mainWindow.analogClockWidget.setClockStyle(style)
            self.mainWindow.previewAnalogClockWidget.setClockStyle(style)

    def _handleApplySettings(self) -> None:
        """Handle the apply settings button click."""
        # Get selected values from settings panel
        newThemeId = self.mainWindow.settingsPanel.getSelectedThemeId()
        newStyleId = self.mainWindow.settingsPanel.getSelectedClockStyleId()
        showSeconds = self.mainWindow.settingsPanel.isShowSecondsChecked()
        showDateInfo = self.mainWindow.settingsPanel.isShowDateInfoChecked()
        timeFormat24 = self.mainWindow.settingsPanel.getSelectedTimeFormat() == 24

        # Update settings
        self.settings.selectedThemeId = newThemeId
        self.settings.selectedClockStyleId = newStyleId
        self.settings.showSeconds = showSeconds
        self.settings.showDateInfo = showDateInfo
        self.settings.use24HourFormat = timeFormat24

        # Update theme service
        self.themeService.setCurrentTheme(newThemeId)
        self.themeService.setCurrentClockStyle(newStyleId)

        # Apply theme and style to UI
        self._applyCurrentThemeAndStyle()

        # Update clocks with new settings
        self.updateClock()

    def showMainWindow(self) -> None:
        """Show the main application window."""
        self.mainWindow.show()

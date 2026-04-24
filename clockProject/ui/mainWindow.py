"""Main application window."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ui.widgets.alarmPanel import AlarmPanel
from ui.widgets.analogClockWidget import AnalogClockWidget
from ui.widgets.calendarWidget import CalendarWidget
from ui.widgets.digitalClockWidget import DigitalClockWidget
from ui.widgets.settingsPanel import SettingsPanel
from ui.widgets.stopwatchPanel import StopwatchPanel
from ui.widgets.timerPanel import TimerPanel
from ui.widgets.timezonePanel import TimezonePanel


class MainWindow(QMainWindow):
    """Composes the high-level UI sections of the clock application."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Reloj Multifunción")
        self.resize(1200, 720)

        self._buildUi()

    def _buildUi(self) -> None:
        rootWidget = QWidget()
        rootLayout = QVBoxLayout(rootWidget)

        topLayout = QHBoxLayout()
        topLayout.addWidget(self._createGroupBox("Reloj analógico", AnalogClockWidget()))
        topLayout.addWidget(self._createGroupBox("Reloj digital", DigitalClockWidget()))
        topLayout.addWidget(self._createGroupBox("Calendario y fecha", CalendarWidget()))
        rootLayout.addLayout(topLayout)

        self.tabs = QTabWidget()

        self.alarmPanel = AlarmPanel()
        self.stopwatchPanel = StopwatchPanel()
        self.timerPanel = TimerPanel()
        self.timezonePanel = TimezonePanel()
        self.settingsPanel = SettingsPanel()

        self.tabs.addTab(self.alarmPanel, "Alarmas")
        self.tabs.addTab(self.stopwatchPanel, "Cronómetro")
        self.tabs.addTab(self.timerPanel, "Temporizador")
        self.tabs.addTab(self.timezonePanel, "Zona horaria")
        self.tabs.addTab(self.settingsPanel, "Configuración")

        rootLayout.addWidget(self.tabs)

        self.setCentralWidget(rootWidget)
        self.statusBar().showMessage("Aplicación inicializada")

    def _createGroupBox(self, title: str, contentWidget: QWidget) -> QGroupBox:
        """Create a titled section with the provided content widget."""
        groupBox = QGroupBox(title)
        layout = QVBoxLayout(groupBox)
        layout.addWidget(contentWidget)
        return groupBox

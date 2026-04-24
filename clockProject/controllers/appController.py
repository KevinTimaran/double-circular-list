"""Application controller that wires services and UI."""

from __future__ import annotations

from models.clockSettings import ClockSettings
from services.alarmService import AlarmService
from services.animationService import AnimationService
from services.clockService import ClockService
from services.countdownService import CountdownService
from services.historyService import HistoryService
from services.stopwatchService import StopwatchService
from services.themeService import ThemeService
from services.timezoneService import TimezoneService
from ui.mainWindow import MainWindow


class AppController:
    """Coordinates services and user interface interactions."""

    def __init__(self) -> None:
        self.settings = ClockSettings()

        self.clockService = ClockService(self.settings)
        self.alarmService = AlarmService()
        self.stopwatchService = StopwatchService()
        self.countdownService = CountdownService()
        self.timezoneService = TimezoneService()
        self.themeService = ThemeService()
        self.historyService = HistoryService()
        self.animationService = AnimationService()

        self.mainWindow = MainWindow()
        self._connectSignals()

    def _connectSignals(self) -> None:
        """Connect UI signals to controller handlers (scaffold stage)."""
        # Connections will be implemented during feature development.
        return

    def showMainWindow(self) -> None:
        """Show the main application window."""
        self.mainWindow.show()

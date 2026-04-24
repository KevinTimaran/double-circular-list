"""Service layer for current date/time behavior."""

from __future__ import annotations

from datetime import datetime

from models.clockSettings import ClockSettings


class ClockService:
    """Provides date/time values based on automatic or manual mode."""

    def __init__(self, settings: ClockSettings) -> None:
        self.settings = settings

    def getCurrentDateTime(self) -> datetime:
        """Return current date/time according to the active mode."""
        if self.settings.automaticMode:
            return datetime.now()

        return self.settings.manualDateTime or datetime.now()

    def setManualDateTime(self, dateTimeValue: datetime) -> None:
        """Set a manual date/time reference for manual mode."""
        self.settings.manualDateTime = dateTimeValue

    def setAutomaticMode(self, enabled: bool) -> None:
        """Enable or disable automatic system time mode."""
        self.settings.automaticMode = enabled

    def toggleMode(self) -> bool:
        """Toggle between automatic and manual mode and return new state."""
        self.settings.automaticMode = not self.settings.automaticMode
        return self.settings.automaticMode

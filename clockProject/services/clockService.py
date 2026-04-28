"""Service layer for current date/time behavior."""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from models.clockSettings import ClockSettings
from services.timezoneService import TimezoneService


class ClockService:
    """Provides date/time values based on automatic or manual mode."""

    def __init__(self, settings: ClockSettings, timezoneService: TimezoneService) -> None:
        self.settings = settings
        self.timezoneService = timezoneService

    def getCurrentDateTime(self) -> datetime:
        """Return current date/time according to the active mode."""
        timezoneItem = self.timezoneService.getCurrentTimezone()
        timezoneInfo = ZoneInfo(timezoneItem.timezoneCode) if timezoneItem is not None else None

        if self.settings.automaticMode:
            return datetime.now(timezoneInfo) if timezoneInfo is not None else datetime.now()

        if self.settings.manualDateTime is None:
            return datetime.now(timezoneInfo) if timezoneInfo is not None else datetime.now()

        if self.settings.manualStartedAt is None:
            return self.settings.manualDateTime

        elapsed = datetime.now() - self.settings.manualStartedAt
        return self.settings.manualDateTime + elapsed

    def getCurrentTimeText(self, dateTimeValue: datetime | None = None) -> str:
        """Return the current time as text for the digital clock."""
        dateTimeValue = dateTimeValue or self.getCurrentDateTime()

        if self.settings.use24HourFormat:
            if self.settings.showSeconds:
                return dateTimeValue.strftime("%H:%M:%S")
            return dateTimeValue.strftime("%H:%M")

        if self.settings.showSeconds:
            return dateTimeValue.strftime("%I:%M:%S %p")
        return dateTimeValue.strftime("%I:%M %p")

    def getCurrentDateText(self, dateTimeValue: datetime | None = None) -> str:
        """Return the current date as text for the date section."""
        dateTimeValue = dateTimeValue or self.getCurrentDateTime()
        return dateTimeValue.strftime("%d/%m/%Y")

    def setAutomaticMode(self) -> None:
        """Use the real system date and time."""
        self.settings.automaticMode = True
        self.settings.manualStartedAt = None

    def setManualMode(self, dateTimeValue: datetime) -> None:
        """Use a custom date and time value and let it continue running."""
        self.settings.automaticMode = False
        self.settings.manualDateTime = dateTimeValue
        self.settings.manualStartedAt = datetime.now()

    def setManualDateTime(self, dateTimeValue: datetime) -> None:
        """Store a custom date/time value without changing mode."""
        self.settings.manualDateTime = dateTimeValue
        self.settings.manualStartedAt = datetime.now()

    def isAutomaticMode(self) -> bool:
        """Return True when the clock is using system time."""
        return self.settings.automaticMode

    def toggleMode(self) -> bool:
        """Toggle between automatic and manual mode and return new state."""
        if self.settings.automaticMode:
            self.setManualMode(datetime.now())
        else:
            self.setAutomaticMode()

        return self.settings.automaticMode
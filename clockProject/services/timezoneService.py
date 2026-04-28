"""Service layer for timezone management and navigation."""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

from dataStructures.doublyCircularList import DoublyCircularList
from models.timezoneItem import TimezoneItem


class TimezoneService:
    """Manages timezone data and circular navigation."""

    def __init__(self, selectedTimezoneCode: str = "America/Bogota") -> None:
        self.timezoneNavigation: DoublyCircularList[TimezoneItem] = DoublyCircularList()
        self.loadDefaultTimezones()
        self.setCurrentTimezone(selectedTimezoneCode)

    def loadDefaultTimezones(self) -> None:
        """Load an initial set of timezone options."""
        self.timezoneNavigation = DoublyCircularList()
        defaults = [
            TimezoneItem(cityName="Bogotá", timezoneCode="America/Bogota"),
            TimezoneItem(cityName="Nueva York", timezoneCode="America/New_York"),
            TimezoneItem(cityName="Londres", timezoneCode="Europe/London"),
            TimezoneItem(cityName="Madrid", timezoneCode="Europe/Madrid"),
            TimezoneItem(cityName="Tokio", timezoneCode="Asia/Tokyo"),
        ]

        for timezone in defaults:
            self.timezoneNavigation.append(timezone)

    def getAllTimezones(self) -> list[TimezoneItem]:
        """Return all known timezone items."""
        return list(self.timezoneNavigation)

    def getCurrentTimezone(self) -> Optional[TimezoneItem]:
        """Return the current timezone in navigation cursor."""
        return self.timezoneNavigation.getCurrent()

    def moveNextTimezone(self) -> Optional[TimezoneItem]:
        """Move to the next timezone in circular order."""
        return self.timezoneNavigation.moveNext()

    def movePreviousTimezone(self) -> Optional[TimezoneItem]:
        """Move to the previous timezone in circular order."""
        return self.timezoneNavigation.movePrevious()

    def setCurrentTimezone(self, timezoneCode: str) -> Optional[TimezoneItem]:
        """Move the cursor to the timezone with the given code if it exists."""
        timezones = self.getAllTimezones()
        for _ in range(len(timezones)):
            currentTimezone = self.getCurrentTimezone()
            if currentTimezone is None:
                break
            if currentTimezone.timezoneCode == timezoneCode:
                return currentTimezone
            self.moveNextTimezone()

        if timezones:
            return self.getCurrentTimezone()

        return None

    def getCurrentDateTime(self) -> datetime:
        """Return the current date/time in the active timezone."""
        currentTimezone = self.getCurrentTimezone()
        if currentTimezone is None:
            return datetime.now()

        return datetime.now(ZoneInfo(currentTimezone.timezoneCode))

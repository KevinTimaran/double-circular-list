"""Service layer for timezone management and navigation."""

from __future__ import annotations

from typing import Optional

from dataStructures.doublyCircularList import DoublyCircularList
from models.timezoneItem import TimezoneItem


class TimezoneService:
    """Manages timezone data and circular navigation."""

    def __init__(self) -> None:
        self.timezones: list[TimezoneItem] = []
        self.timezoneNavigation: DoublyCircularList[TimezoneItem] = DoublyCircularList()
        self.loadDefaultTimezones()

    def loadDefaultTimezones(self) -> None:
        """Load an initial set of timezone options."""
        defaults = [
            TimezoneItem(code="UTC", cityName="UTC", offsetHours=0),
            TimezoneItem(code="COT", cityName="Bogota", offsetHours=-5),
            TimezoneItem(code="CET", cityName="Madrid", offsetHours=1),
            TimezoneItem(code="JST", cityName="Tokyo", offsetHours=9),
        ]

        for timezone in defaults:
            self.addTimezone(timezone)

    def addTimezone(self, timezoneItem: TimezoneItem) -> None:
        """Add a new timezone to the service."""
        self.timezones.append(timezoneItem)
        self.timezoneNavigation.append(timezoneItem)

    def getAllTimezones(self) -> list[TimezoneItem]:
        """Return all known timezone items."""
        return list(self.timezones)

    def getCurrentTimezone(self) -> Optional[TimezoneItem]:
        """Return the current timezone in navigation cursor."""
        return self.timezoneNavigation.getCurrent()

    def moveToNextTimezone(self) -> Optional[TimezoneItem]:
        """Move to the next timezone in circular order."""
        return self.timezoneNavigation.moveNext()

    def moveToPreviousTimezone(self) -> Optional[TimezoneItem]:
        """Move to the previous timezone in circular order."""
        return self.timezoneNavigation.movePrevious()

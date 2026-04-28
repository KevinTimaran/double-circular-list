"""Alarm domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Alarm:
    """Represents an alarm configured by the user."""

    alarmId: int
    hour: int
    minute: int
    label: str
    enabled: bool = True

    def getDisplayTime(self) -> str:
        """Return the alarm time as a 12-hour formatted string."""
        displayHour = self.hour % 12
        if displayHour == 0:
            displayHour = 12

        period = "AM" if self.hour < 12 else "PM"
        return f"{displayHour:02d}:{self.minute:02d} {period}"

"""Timezone model for timezone selection."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TimezoneItem:
    """Represents a timezone option in the app."""

    code: str
    cityName: str
    offsetHours: int
    offsetMinutes: int = 0

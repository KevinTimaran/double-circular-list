"""Timezone model for timezone selection."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TimezoneItem:
    """Represents a timezone option in the app."""

    cityName: str
    timezoneCode: str
    displayLabel: str = ""

    def __post_init__(self) -> None:
        if not self.displayLabel:
            self.displayLabel = f"{self.cityName} / {self.timezoneCode}"

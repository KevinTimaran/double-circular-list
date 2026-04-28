"""Clock settings model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ClockSettings:
    """Stores user-configurable settings for the clock application."""

    automaticMode: bool = True
    manualDateTime: Optional[datetime] = None
    manualStartedAt: Optional[datetime] = None
    showSeconds: bool = True
    use24HourFormat: bool = True
    selectedThemeId: int = 1
    selectedClockStyleId: int = 1
    selectedTimezoneCode: str = "America/Bogota"
    showDateInfo: bool = True

"""Clock settings model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ClockSettings:
    """Stores user-configurable settings for the clock application."""

    automaticMode: bool = True
    use24HourFormat: bool = True
    selectedThemeId: int = 1
    selectedTimezoneCode: str = "UTC"
    manualDateTime: Optional[datetime] = None

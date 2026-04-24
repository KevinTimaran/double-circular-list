"""Alarm domain model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import time


@dataclass
class Alarm:
    """Represents an alarm configured by the user."""

    alarmId: int
    label: str
    alarmTime: time
    enabled: bool = True
    repeatDaily: bool = False

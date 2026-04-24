"""Lap record model for stopwatch history."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LapRecord:
    """Represents a single saved lap from the stopwatch."""

    lapNumber: int
    elapsedSeconds: float
    recordedAt: datetime = field(default_factory=datetime.now)

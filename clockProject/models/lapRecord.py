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

    @property
    def elapsedMilliseconds(self) -> int:
        return int(self.elapsedSeconds * 1000)

    @property
    def formattedElapsedTime(self) -> str:
        total_ms = self.elapsedMilliseconds
        ms = int((total_ms % 1000) / 10)  # two-digit centiseconds
        total_seconds = total_ms // 1000
        secs = total_seconds % 60
        mins = (total_seconds // 60) % 60
        hours = total_seconds // 3600
        return f"{hours:02d}:{mins:02d}:{secs:02d}.{ms:02d}"

    @property
    def timestampText(self) -> str:
        return self.recordedAt.strftime("%Y-%m-%d %H:%M:%S")

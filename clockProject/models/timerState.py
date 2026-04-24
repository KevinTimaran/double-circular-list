"""Timer state model used by stopwatch and countdown services."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TimerState:
    """Stores generic state for time-based operations."""

    totalSeconds: float = 0.0
    remainingSeconds: float = 0.0
    isRunning: bool = False
    isPaused: bool = False

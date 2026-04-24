"""Service layer for stopwatch operations."""

from __future__ import annotations

from time import perf_counter
from typing import Optional

from dataStructures.doublyCircularList import DoublyCircularList
from models.lapRecord import LapRecord


class StopwatchService:
    """Controls stopwatch lifecycle and lap history."""

    def __init__(self) -> None:
        self.elapsedSeconds: float = 0.0
        self.isRunning: bool = False
        self.isPaused: bool = False
        self._startTimestamp: Optional[float] = None
        self._pauseTimestamp: Optional[float] = None
        self._lapCounter: int = 0
        self.lapHistory: DoublyCircularList[LapRecord] = DoublyCircularList()

    def start(self) -> None:
        """Start the stopwatch from zero."""
        self.reset()
        self.isRunning = True
        self.isPaused = False
        self._startTimestamp = perf_counter()

    def pause(self) -> None:
        """Pause the stopwatch and keep elapsed time."""
        if not self.isRunning or self.isPaused:
            return

        self._updateElapsed()
        self.isPaused = True
        self._pauseTimestamp = perf_counter()

    def resume(self) -> None:
        """Resume the stopwatch after a pause."""
        if not self.isRunning or not self.isPaused:
            return

        now = perf_counter()
        pauseDuration = now - (self._pauseTimestamp or now)

        if self._startTimestamp is not None:
            self._startTimestamp += pauseDuration

        self.isPaused = False
        self._pauseTimestamp = None

    def reset(self) -> None:
        """Reset the stopwatch state and clear laps."""
        self.elapsedSeconds = 0.0
        self.isRunning = False
        self.isPaused = False
        self._startTimestamp = None
        self._pauseTimestamp = None
        self._lapCounter = 0
        self.lapHistory = DoublyCircularList()

    def saveLap(self) -> Optional[LapRecord]:
        """Save the current elapsed time as a lap record."""
        if not self.isRunning:
            return None

        self._updateElapsed()
        self._lapCounter += 1

        lapRecord = LapRecord(
            lapNumber=self._lapCounter,
            elapsedSeconds=self.elapsedSeconds,
        )
        self.lapHistory.append(lapRecord)
        return lapRecord

    def getLapHistory(self) -> list[LapRecord]:
        """Return lap records as a regular list."""
        return list(self.lapHistory)

    def moveToNextLap(self) -> Optional[LapRecord]:
        """Move lap cursor to next lap."""
        return self.lapHistory.moveNext()

    def moveToPreviousLap(self) -> Optional[LapRecord]:
        """Move lap cursor to previous lap."""
        return self.lapHistory.movePrevious()

    def getCurrentLap(self) -> Optional[LapRecord]:
        """Return the current lap pointed by the cursor."""
        return self.lapHistory.getCurrent()

    def _updateElapsed(self) -> None:
        """Internal helper to refresh elapsed seconds."""
        if self._startTimestamp is None or self.isPaused:
            return

        self.elapsedSeconds = perf_counter() - self._startTimestamp

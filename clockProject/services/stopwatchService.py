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
        self._isRunning: bool = False
        self._isPaused: bool = False
        self._startTimestamp: Optional[float] = None
        self._pauseTimestamp: Optional[float] = None
        self._lapCounter: int = 0
        self._hasStarted: bool = False
        self.lapHistory: DoublyCircularList[LapRecord] = DoublyCircularList()

    # Lifecycle control
    def start(self) -> None:
        """Start the stopwatch from zero."""
        self.resetTimeOnly()
        self._isRunning = True
        self._isPaused = False
        self._hasStarted = True
        self._startTimestamp = perf_counter()

    def pause(self) -> None:
        """Pause the stopwatch and keep elapsed time."""
        if not self._isRunning or self._isPaused:
            return

        self._updateElapsed()
        self._isPaused = True
        self._pauseTimestamp = perf_counter()

    def resume(self) -> None:
        """Resume the stopwatch after a pause."""
        if not self._isRunning or not self._isPaused:
            return

        now = perf_counter()
        pauseDuration = now - (self._pauseTimestamp or now)

        if self._startTimestamp is not None:
            self._startTimestamp += pauseDuration

        self._isPaused = False
        self._pauseTimestamp = None

    def resetTimeOnly(self) -> None:
        """Reset the stopwatch state without clearing lap history."""
        self.elapsedSeconds = 0.0
        self._isRunning = False
        self._isPaused = False
        self._startTimestamp = None
        self._pauseTimestamp = None

    def clearLapHistory(self) -> None:
        """Remove all saved laps and reset lap numbering."""
        self.lapHistory = DoublyCircularList()
        self._lapCounter = 0

    def reset(self) -> None:
        """Backward-compatible alias for resetting time only."""
        self.resetTimeOnly()

    # Lap operations
    def addLap(self) -> Optional[LapRecord]:
        """Save the current elapsed time as a lap record."""
        # Allow lap saving when running or paused, but not if not started
        if not self._isRunning:
            return None

        self._updateElapsed()
        self._lapCounter += 1

        lapRecord = LapRecord(
            lapNumber=self._lapCounter,
            elapsedSeconds=self.elapsedSeconds,
        )
        self.lapHistory.append(lapRecord)
        return lapRecord

    def removeLap(self, lapNumber: int) -> bool:
        """Remove a lap from the history by lap number."""
        for lap in self.lapHistory:
            if lap.lapNumber == lapNumber:
                return self.lapHistory.remove(lap)

        return False

    # Backwards-compatible alias
    def saveLap(self) -> Optional[LapRecord]:
        return self.addLap()

    # Navigation and accessors
    def getAllLaps(self) -> list[LapRecord]:
        """Return lap records as a regular list."""
        return list(self.lapHistory)

    def moveNextLap(self) -> Optional[LapRecord]:
        """Move lap cursor to next lap."""
        return self.lapHistory.moveNext()

    def movePreviousLap(self) -> Optional[LapRecord]:
        """Move lap cursor to previous lap."""
        return self.lapHistory.movePrevious()

    def getCurrentLap(self) -> Optional[LapRecord]:
        """Return the current lap pointed by the cursor."""
        return self.lapHistory.getCurrent()

    def hasStarted(self) -> bool:
        """Return True if the stopwatch has been started at least once."""
        return self._hasStarted

    # Status and formatting
    def getElapsedMilliseconds(self) -> int:
        self._updateElapsed()
        return int(self.elapsedSeconds * 1000)

    def getFormattedElapsedTime(self) -> str:
        self._updateElapsed()
        total_ms = self.getElapsedMilliseconds()
        ms = int((total_ms % 1000) / 10)
        total_seconds = total_ms // 1000
        secs = total_seconds % 60
        mins = (total_seconds // 60) % 60
        hours = total_seconds // 3600
        return f"{hours:02d}:{mins:02d}:{secs:02d}.{ms:02d}"

    def isRunning(self) -> bool:
        return self._isRunning

    def isPaused(self) -> bool:
        return self._isPaused

    def updateElapsedTime(self) -> None:
        """Public method to force-update internal elapsed value."""
        self._updateElapsed()

    def _updateElapsed(self) -> None:
        """Internal helper to refresh elapsed seconds."""
        if self._startTimestamp is None or self._isPaused:
            return

        self.elapsedSeconds = perf_counter() - self._startTimestamp

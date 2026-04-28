"""Service layer for Pomodoro session management."""

from __future__ import annotations

from typing import Optional

from dataStructures.doublyCircularList import DoublyCircularList
from models.pomodoroPhase import PomodoroPhase


class PomodoroService:
    """Manages the Pomodoro cycle using a circular list of phases."""

    def __init__(self) -> None:
        self.phases: DoublyCircularList[PomodoroPhase] = DoublyCircularList()
        self._isRunning: bool = False
        self._isPaused: bool = False
        
        self.remainingSeconds: int = 0
        self.completedPomodoros: int = 0
        
        self._buildStandardCycle()
        self.reset()

    def _buildStandardCycle(self) -> None:
        """Build the classic 8-step Pomodoro cycle."""
        # Focus, Short Break, Focus, Short Break, Focus, Short Break, Focus, Long Break
        cycle = [
            ("focus", "Tiempo de Enfoque", 25, "#ef4444"),
            ("short_break", "Descanso Corto", 5, "#22c55e"),
            ("focus", "Tiempo de Enfoque", 25, "#ef4444"),
            ("short_break", "Descanso Corto", 5, "#22c55e"),
            ("focus", "Tiempo de Enfoque", 25, "#ef4444"),
            ("short_break", "Descanso Corto", 5, "#22c55e"),
            ("focus", "Tiempo de Enfoque", 25, "#ef4444"),
            ("long_break", "Descanso Largo", 15, "#3b82f6"),
        ]
        
        for pType, pName, pDuration, pColor in cycle:
            phase = PomodoroPhase(pType, pName, pDuration, pColor)
            self.phases.append(phase)

    def updatePhaseDurations(self, focusMin: int, shortBreakMin: int, longBreakMin: int) -> None:
        """Update the durations of all phases based on type and adjust current time if stopped."""
        node = self.phases.head
        if not node:
            return

        while True:
            phase = node.data
            if phase.phaseType == "focus":
                phase.durationMinutes = focusMin
            elif phase.phaseType == "short_break":
                phase.durationMinutes = shortBreakMin
            elif phase.phaseType == "long_break":
                phase.durationMinutes = longBreakMin
            
            node = node.next
            if node == self.phases.head:
                break
        
        # If we are not running, update the current phase's remaining seconds
        if not self._isRunning:
            current = self.getCurrentPhase()
            if current:
                # If we are exactly at the start of the phase or we just updated the duration
                # the simplest logic is to just reset to the new total.
                # However, if they paused midway, resetting might lose progress.
                # For simplicity, if they change the settings, we'll reset the current phase's time
                # to the new max. This is standard for most timers.
                self.remainingSeconds = current.totalSeconds

    def getCurrentPhase(self) -> Optional[PomodoroPhase]:
        """Return the current active phase."""
        return self.phases.getCurrent()

    def start(self) -> None:
        """Start or resume the current phase."""
        if not self._isRunning and not self._isPaused:
            self._isRunning = True
        elif self._isPaused:
            self._isPaused = False
            self._isRunning = True

    def pause(self) -> None:
        """Pause the timer."""
        if self._isRunning:
            self._isPaused = True
            self._isRunning = False

    def toggle(self) -> None:
        """Toggle between play and pause."""
        if self.isRunning():
            self.pause()
        else:
            self.start()

    def reset(self) -> None:
        """Reset to the beginning of the very first phase, clear counters."""
        self._isRunning = False
        self._isPaused = False
        self.completedPomodoros = 0
        
        # Move cursor to the very first node (head)
        self.phases.current = self.phases.head
        phase = self.getCurrentPhase()
        if phase:
            self.remainingSeconds = phase.totalSeconds

    def resetCurrentPhase(self) -> None:
        """Reset the time of the current phase without changing phases."""
        self._isRunning = False
        self._isPaused = False
        phase = self.getCurrentPhase()
        if phase:
            self.remainingSeconds = phase.totalSeconds

    def skipPhase(self) -> None:
        """Manually jump to the next phase."""
        self._advancePhase(manual=True)

    def tick(self) -> bool:
        """Advance time by one second. Return True if phase completed this tick."""
        if not self.isRunning():
            return False

        if self.remainingSeconds > 0:
            self.remainingSeconds -= 1
            if self.remainingSeconds == 0:
                self._advancePhase(manual=False)
                return True
        return False

    def _advancePhase(self, manual: bool = False) -> None:
        """Move to the next phase in the circular list."""
        current = self.getCurrentPhase()
        if current and current.phaseType == "focus" and not manual:
            # Only count as completed if it finished naturally
            self.completedPomodoros += 1

        self.phases.moveNext()
        nextPhase = self.getCurrentPhase()
        
        # Stop the timer when changing phases, user must press play again
        self._isRunning = False
        self._isPaused = False
        if nextPhase:
            self.remainingSeconds = nextPhase.totalSeconds

    def isRunning(self) -> bool:
        return self._isRunning

    def isPaused(self) -> bool:
        return self._isPaused

    def getFormattedTime(self) -> str:
        """Return MM:SS format of remaining time."""
        mins = self.remainingSeconds // 60
        secs = self.remainingSeconds % 60
        return f"{mins:02d}:{secs:02d}"

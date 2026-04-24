"""Service layer for countdown timer behavior."""

from __future__ import annotations


class CountdownService:
    """Handles countdown timer state transitions."""

    def __init__(self) -> None:
        self.durationSeconds: int = 0
        self.remainingSeconds: int = 0
        self.isRunning: bool = False
        self.isPaused: bool = False

    def setDuration(self, totalSeconds: int) -> None:
        """Set countdown duration in seconds."""
        self.durationSeconds = max(0, totalSeconds)
        self.remainingSeconds = self.durationSeconds

    def start(self) -> None:
        """Start countdown from remaining time."""
        if self.remainingSeconds <= 0:
            return

        self.isRunning = True
        self.isPaused = False

    def pause(self) -> None:
        """Pause the countdown."""
        if not self.isRunning:
            return

        self.isPaused = True
        self.isRunning = False

    def resume(self) -> None:
        """Resume countdown after pause."""
        if self.remainingSeconds <= 0 or not self.isPaused:
            return

        self.isPaused = False
        self.isRunning = True

    def reset(self) -> None:
        """Reset countdown to original duration."""
        self.remainingSeconds = self.durationSeconds
        self.isRunning = False
        self.isPaused = False

    def tick(self) -> int:
        """Decrease countdown by one second and return remaining seconds."""
        if not self.isRunning or self.remainingSeconds <= 0:
            return self.remainingSeconds

        self.remainingSeconds -= 1

        if self.remainingSeconds <= 0:
            self.remainingSeconds = 0
            self.isRunning = False
            self.isPaused = False

        return self.remainingSeconds

"""Model representing a single phase in the Pomodoro cycle."""

from __future__ import annotations


class PomodoroPhase:
    """Encapsulates information about a specific Pomodoro phase."""

    def __init__(self, phaseType: str, name: str, durationMinutes: int, colorHex: str) -> None:
        self.phaseType = phaseType  # "focus", "short_break", "long_break"
        self.name = name
        self.durationMinutes = durationMinutes
        self.colorHex = colorHex

    @property
    def totalSeconds(self) -> int:
        return self.durationMinutes * 60

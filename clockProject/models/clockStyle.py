"""Clock style/design preset model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ClockStyle:
    """Represents a visual style preset for the analog clock."""

    styleId: int
    displayName: str
    dialBackground: str
    ringColor: str
    numberColor: str
    hourHandColor: str
    minuteHandColor: str
    secondHandColor: str
    showNumbers: bool = True
    showMinuteMarks: bool = True
    showDateInfo: bool = True
    showSeconds: bool = True

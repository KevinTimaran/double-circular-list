"""Theme domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Theme:
    """Represents a visual theme for the application UI."""

    themeId: int
    displayName: str
    windowBackground: str
    panelBackground: str
    textColor: str
    accentColor: str
    styleSheet: str = ""

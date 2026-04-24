"""Theme domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Theme:
    """Represents a visual theme for the application."""

    themeId: int
    displayName: str
    styleSheet: str

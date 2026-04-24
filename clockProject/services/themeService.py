"""Service layer for theme navigation and selection."""

from __future__ import annotations

from typing import Optional

from dataStructures.doublyCircularList import DoublyCircularList
from models.theme import Theme


class ThemeService:
    """Manages available themes with circular navigation."""

    def __init__(self) -> None:
        self.themes: list[Theme] = []
        self.themeNavigation: DoublyCircularList[Theme] = DoublyCircularList()
        self.loadDefaultThemes()

    def loadDefaultThemes(self) -> None:
        """Load starter themes for the scaffold."""
        defaultThemes = [
            Theme(themeId=1, displayName="Claro", styleSheet="QWidget { background-color: #f5f5f5; }"),
            Theme(themeId=2, displayName="Oscuro", styleSheet="QWidget { background-color: #1f1f1f; color: #f5f5f5; }"),
            Theme(themeId=3, displayName="Azul", styleSheet="QWidget { background-color: #eaf3ff; }"),
        ]

        for theme in defaultThemes:
            self.addTheme(theme)

    def addTheme(self, theme: Theme) -> None:
        """Add a theme to the service and navigation list."""
        self.themes.append(theme)
        self.themeNavigation.append(theme)

    def getCurrentTheme(self) -> Optional[Theme]:
        """Return currently selected theme."""
        return self.themeNavigation.getCurrent()

    def moveToNextTheme(self) -> Optional[Theme]:
        """Move to next theme and return it."""
        return self.themeNavigation.moveNext()

    def moveToPreviousTheme(self) -> Optional[Theme]:
        """Move to previous theme and return it."""
        return self.themeNavigation.movePrevious()

    def applyTheme(self, theme: Theme) -> str:
        """Return style sheet string for future UI application."""
        return theme.styleSheet

"""Service layer for theme and clock style navigation and selection."""

from __future__ import annotations

from typing import Optional

from dataStructures.doublyCircularList import DoublyCircularList
from models.theme import Theme
from models.clockStyle import ClockStyle


class ThemeService:
    """Manages available themes and clock styles with circular navigation."""

    def __init__(self) -> None:
        self.themes: list[Theme] = []
        self.themeNavigation: DoublyCircularList[Theme] = DoublyCircularList()
        self.clockStyles: list[ClockStyle] = []
        self.styleNavigation: DoublyCircularList[ClockStyle] = DoublyCircularList()
        self.currentThemeId: int = 1
        self.currentStyleId: int = 1
        self.loadDefaultThemes()
        self.loadDefaultClockStyles()

    def loadDefaultThemes(self) -> None:
        """Load predefined premium application themes."""
        
        base_qss_template = """
            QWidget {{
                background-color: {bg_color};
                color: {text_color};
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Arial, sans-serif;
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {btn_bg};
                border: 1px solid {border_color};
                border-radius: 6px;
                color: {text_color};
                padding: 8px 16px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
                border-color: {accent_color};
            }}
            QPushButton:pressed {{
                background-color: {btn_bg};
            }}
            QTabWidget::pane {{
                border: 1px solid {border_color};
                border-radius: 8px;
                background-color: {bg_color};
                margin-top: -1px;
            }}
            QTabBar::tab {{
                background: {bg_color};
                color: {text_dim};
                border: 1px solid transparent;
                padding: 10px 20px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }}
            QTabBar::tab:selected {{
                color: {text_color};
                background: {panel_bg};
                border: 1px solid {border_color};
                border-bottom-color: {panel_bg};
                font-weight: bold;
            }}
            QTabBar::tab:hover:!selected {{
                color: {text_color};
                background: {panel_bg};
            }}
            QListWidget {{
                background-color: {panel_bg};
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 4px;
                outline: none;
            }}
            QListWidget::item {{
                padding: 10px;
                border-radius: 6px;
                margin-bottom: 2px;
            }}
            QListWidget::item:selected {{
                background-color: {accent_color};
                color: #ffffff;
            }}
            QListWidget::item:hover:!selected {{
                background-color: {btn_bg};
            }}
            QComboBox, QSpinBox, QTimeEdit, QLineEdit {{
                background-color: {btn_bg};
                border: 1px solid {border_color};
                border-radius: 6px;
                padding: 6px;
                color: {text_color};
            }}
            QComboBox:hover, QTimeEdit:hover, QLineEdit:hover {{
                border-color: {accent_color};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid {border_color};
                background-color: {btn_bg};
            }}
            QCheckBox::indicator:checked {{
                background-color: {accent_color};
                border-color: {accent_color};
            }}
            QSpinBox::up-button, QTimeEdit::up-button, QSpinBox::down-button, QTimeEdit::down-button {{
                background-color: #94a3b8;
                border-left: 1px solid {border_color};
                width: 20px;
            }}
            QSpinBox::up-button:hover, QTimeEdit::up-button:hover, QSpinBox::down-button:hover, QTimeEdit::down-button:hover {{
                background-color: #cbd5e1;
            }}
        """

        defaultThemes = [
            Theme(
                themeId=1,
                displayName="Midnight Onyx",
                windowBackground="#09090b",
                panelBackground="#18181b",
                textColor="#f4f4f5",
                accentColor="#3b82f6",
                styleSheet=base_qss_template.format(
                    bg_color="#09090b",
                    panel_bg="#18181b",
                    text_color="#f4f4f5",
                    text_dim="#a1a1aa",
                    btn_bg="#27272a",
                    btn_hover="#3f3f46",
                    border_color="#3f3f46",
                    accent_color="#3b82f6",
                ),
            ),
            Theme(
                themeId=2,
                displayName="Executive Slate",
                windowBackground="#0f172a",
                panelBackground="#1e293b",
                textColor="#f8fafc",
                accentColor="#0ea5e9",
                styleSheet=base_qss_template.format(
                    bg_color="#0f172a",
                    panel_bg="#1e293b",
                    text_color="#f8fafc",
                    text_dim="#94a3b8",
                    btn_bg="#334155",
                    btn_hover="#475569",
                    border_color="#475569",
                    accent_color="#0ea5e9",
                ),
            ),
            Theme(
                themeId=3,
                displayName="Luxury Gold",
                windowBackground="#171717",
                panelBackground="#262626",
                textColor="#fafafa",
                accentColor="#d4af37",
                styleSheet=base_qss_template.format(
                    bg_color="#171717",
                    panel_bg="#262626",
                    text_color="#fafafa",
                    text_dim="#a3a3a3",
                    btn_bg="#404040",
                    btn_hover="#525252",
                    border_color="#525252",
                    accent_color="#d4af37",
                ),
            ),
        ]

        for theme in defaultThemes:
            self.addTheme(theme)

    def loadDefaultClockStyles(self) -> None:
        """Load predefined clock style presets inspired by different watch designs."""
        # Clásico elegante - inspired by classic elegant watches
        self.addClockStyle(
            ClockStyle(
                styleId=1,
                displayName="Clásico elegante",
                dialBackground="#f5f0e8",
                ringColor="#c9a961",
                numberColor="#2c2416",
                hourHandColor="#8b7355",
                minuteHandColor="#3d3428",
                secondHandColor="#d84040",
                showNumbers=True,
                showMinuteMarks=True,
                showDateInfo=True,
            )
        )

        # Deportivo - inspired by sporty watches
        self.addClockStyle(
            ClockStyle(
                styleId=2,
                displayName="Deportivo",
                dialBackground="#2d2d2d",
                ringColor="#00d9ff",
                numberColor="#f0f0f0",
                hourHandColor="#ff6b35",
                minuteHandColor="#f0f0f0",
                secondHandColor="#00ff00",
                showNumbers=True,
                showMinuteMarks=True,
                showDateInfo=False,
            )
        )

        # Minimalista - inspired by minimalist watches
        self.addClockStyle(
            ClockStyle(
                styleId=3,
                displayName="Minimalista",
                dialBackground="#ffffff",
                ringColor="#e0e0e0",
                numberColor="#333333",
                hourHandColor="#000000",
                minuteHandColor="#000000",
                secondHandColor="#666666",
                showNumbers=True,
                showMinuteMarks=False,
                showDateInfo=False,
            )
        )

        # Vintage - inspired by vintage watches
        self.addClockStyle(
            ClockStyle(
                styleId=4,
                displayName="Vintage",
                dialBackground="#f9f3ed",
                ringColor="#b8860b",
                numberColor="#3d3b37",
                hourHandColor="#8b7765",
                minuteHandColor="#4a4540",
                secondHandColor="#c85040",
                showNumbers=True,
                showMinuteMarks=True,
                showDateInfo=True,
            )
        )

        # Premium moderno - inspired by modern luxury watches
        self.addClockStyle(
            ClockStyle(
                styleId=5,
                displayName="Premium moderno",
                dialBackground="#1a1a1a",
                ringColor="#c0c0c0",
                numberColor="#e8e8e8",
                hourHandColor="#ffffff",
                minuteHandColor="#e8e8e8",
                secondHandColor="#ff2e2e",
                showNumbers=True,
                showMinuteMarks=True,
                showDateInfo=True,
            )
        )

    def addTheme(self, theme: Theme) -> None:
        """Add a theme to the service and navigation list."""
        self.themes.append(theme)
        self.themeNavigation.append(theme)

    def addClockStyle(self, style: ClockStyle) -> None:
        """Add a clock style to the service and navigation list."""
        self.clockStyles.append(style)
        self.styleNavigation.append(style)

    # Theme management

    def getCurrentTheme(self) -> Optional[Theme]:
        """Return currently selected theme."""
        for theme in self.themes:
            if theme.themeId == self.currentThemeId:
                return theme
        return None

    def getThemeById(self, themeId: int) -> Optional[Theme]:
        """Get a theme by its ID."""
        for theme in self.themes:
            if theme.themeId == themeId:
                return theme
        return None

    def setCurrentTheme(self, themeId: int) -> Optional[Theme]:
        """Set the current theme by ID."""
        theme = self.getThemeById(themeId)
        if theme is not None:
            self.currentThemeId = themeId
        return theme

    def getAllThemes(self) -> list[Theme]:
        """Return all available themes."""
        return self.themes

    def moveToNextTheme(self) -> Optional[Theme]:
        """Move to next theme and return it."""
        return self.themeNavigation.moveNext()

    def moveToPreviousTheme(self) -> Optional[Theme]:
        """Move to previous theme and return it."""
        return self.themeNavigation.movePrevious()

    # Clock style management

    def getCurrentClockStyle(self) -> Optional[ClockStyle]:
        """Return currently selected clock style."""
        for style in self.clockStyles:
            if style.styleId == self.currentStyleId:
                return style
        return None

    def getClockStyleById(self, styleId: int) -> Optional[ClockStyle]:
        """Get a clock style by its ID."""
        for style in self.clockStyles:
            if style.styleId == styleId:
                return style
        return None

    def setCurrentClockStyle(self, styleId: int) -> Optional[ClockStyle]:
        """Set the current clock style by ID."""
        style = self.getClockStyleById(styleId)
        if style is not None:
            self.currentStyleId = styleId
        return style

    def getAllClockStyles(self) -> list[ClockStyle]:
        """Return all available clock styles."""
        return self.clockStyles

    def moveToNextClockStyle(self) -> Optional[ClockStyle]:
        """Move to next clock style and return it."""
        return self.styleNavigation.moveNext()

    def moveToPreviousClockStyle(self) -> Optional[ClockStyle]:
        """Move to previous clock style and return it."""
        return self.styleNavigation.movePrevious()

    def applyTheme(self, theme: Theme) -> str:
        """Return style sheet string for UI application."""
        return theme.styleSheet

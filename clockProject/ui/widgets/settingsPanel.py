"""Settings panel widget."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QRadioButton,
    QButtonGroup,
    QHBoxLayout,
)
from PySide6.QtCore import Signal


class SettingsPanel(QWidget):
    """Provides controls for application and clock configuration."""

    settingsChanged = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._buildUi()
        self._connectSignals()

    def _buildUi(self) -> None:
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(16)
        mainLayout.setContentsMargins(16, 16, 16, 16)

        # Themes section
        themeSectionLayout = QFormLayout()
        self.themeComboBox = QComboBox()
        themeSectionLayout.addRow("Tema de aplicación:", self.themeComboBox)
        mainLayout.addLayout(themeSectionLayout)

        # Clock styles section
        styleSectionLayout = QFormLayout()
        self.clockStyleComboBox = QComboBox()
        styleSectionLayout.addRow("Estilo del reloj:", self.clockStyleComboBox)
        mainLayout.addLayout(styleSectionLayout)

        # Display options section
        displayOptionsLayout = QFormLayout()

        self.showSecondsCheckBox = QCheckBox("Mostrar segundos")
        self.showSecondsCheckBox.setChecked(True)
        displayOptionsLayout.addRow(self.showSecondsCheckBox)

        self.showDateInfoCheckBox = QCheckBox("Mostrar fecha integrada")
        self.showDateInfoCheckBox.setChecked(True)
        displayOptionsLayout.addRow(self.showDateInfoCheckBox)

        mainLayout.addLayout(displayOptionsLayout)

        # Time format section
        formatLayout = QFormLayout()
        formatButtonGroup = QButtonGroup()

        formatHBoxLayout = QHBoxLayout()
        self.format12HourRadio = QRadioButton("12 horas")
        self.format24HourRadio = QRadioButton("24 horas")
        self.format24HourRadio.setChecked(True)

        formatButtonGroup.addButton(self.format12HourRadio, 12)
        formatButtonGroup.addButton(self.format24HourRadio, 24)

        formatHBoxLayout.addWidget(self.format12HourRadio)
        formatHBoxLayout.addWidget(self.format24HourRadio)
        formatHBoxLayout.addStretch()

        formatLayout.addRow("Formato de hora:", formatHBoxLayout)
        mainLayout.addLayout(formatLayout)

        mainLayout.addStretch()

    def _connectSignals(self) -> None:
        """Connect UI input events to the settingsChanged signal for live updates."""
        self.themeComboBox.currentIndexChanged.connect(lambda _: self.settingsChanged.emit())
        self.clockStyleComboBox.currentIndexChanged.connect(lambda _: self.settingsChanged.emit())
        self.showSecondsCheckBox.stateChanged.connect(lambda _: self.settingsChanged.emit())
        self.showDateInfoCheckBox.stateChanged.connect(lambda _: self.settingsChanged.emit())
        self.format12HourRadio.toggled.connect(lambda _: self.settingsChanged.emit())
        self.format24HourRadio.toggled.connect(lambda _: self.settingsChanged.emit())

    def setThemes(self, themes: list) -> None:
        """Populate the theme combo box with available themes."""
        self.themeComboBox.clear()
        for theme in themes:
            self.themeComboBox.addItem(theme.displayName, theme.themeId)

    def setClockStyles(self, styles: list) -> None:
        """Populate the clock style combo box with available styles."""
        self.clockStyleComboBox.clear()
        for style in styles:
            self.clockStyleComboBox.addItem(style.displayName, style.styleId)

    def getSelectedThemeId(self) -> int:
        """Return the currently selected theme ID."""
        return self.themeComboBox.currentData()

    def getSelectedClockStyleId(self) -> int:
        """Return the currently selected clock style ID."""
        return self.clockStyleComboBox.currentData()

    def isShowSecondsChecked(self) -> bool:
        """Return whether show seconds is checked."""
        return self.showSecondsCheckBox.isChecked()

    def isShowDateInfoChecked(self) -> bool:
        """Return whether show date info is checked."""
        return self.showDateInfoCheckBox.isChecked()

    def getSelectedTimeFormat(self) -> int:
        """Return 12 or 24 based on selected radio button."""
        if self.format12HourRadio.isChecked():
            return 12
        return 24

    def setThemeSelection(self, themeId: int) -> None:
        """Set the theme combo box to the specified theme ID."""
        index = self.themeComboBox.findData(themeId)
        if index >= 0:
            self.themeComboBox.setCurrentIndex(index)

    def setClockStyleSelection(self, styleId: int) -> None:
        """Set the clock style combo box to the specified style ID."""
        index = self.clockStyleComboBox.findData(styleId)
        if index >= 0:
            self.clockStyleComboBox.setCurrentIndex(index)

    def setShowSeconds(self, value: bool) -> None:
        """Set the show seconds checkbox."""
        self.showSecondsCheckBox.setChecked(value)

    def setShowDateInfo(self, value: bool) -> None:
        """Set the show date info checkbox."""
        self.showDateInfoCheckBox.setChecked(value)

    def setTimeFormat(self, is24Hour: bool) -> None:
        """Set the time format (True for 24h, False for 12h)."""
        if is24Hour:
            self.format24HourRadio.setChecked(True)
        else:
            self.format12HourRadio.setChecked(True)

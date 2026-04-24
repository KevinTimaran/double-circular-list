"""Settings panel widget."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SettingsPanel(QWidget):
    """Provides base controls for app configuration."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._buildUi()

    def _buildUi(self) -> None:
        mainLayout = QVBoxLayout(self)

        formLayout = QFormLayout()
        self.automaticModeCheckBox = QCheckBox("Modo automático")
        self.automaticModeCheckBox.setChecked(True)

        self.format24HourCheckBox = QCheckBox("Formato 24 horas")
        self.format24HourCheckBox.setChecked(True)

        formLayout.addRow("Reloj:", self.automaticModeCheckBox)
        formLayout.addRow("Formato:", self.format24HourCheckBox)
        mainLayout.addLayout(formLayout)

        themeLayout = QHBoxLayout()
        self.previousThemeButton = QPushButton("Tema anterior")
        self.nextThemeButton = QPushButton("Tema siguiente")
        themeLayout.addWidget(self.previousThemeButton)
        themeLayout.addWidget(self.nextThemeButton)
        mainLayout.addLayout(themeLayout)

        self.themeNameLabel = QLabel("Tema actual: Claro")
        mainLayout.addWidget(self.themeNameLabel)

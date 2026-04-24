"""Timezone panel widget."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class TimezonePanel(QWidget):
    """Provides base UI for timezone selection and navigation."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._buildUi()

    def _buildUi(self) -> None:
        mainLayout = QVBoxLayout(self)

        self.currentTimezoneLabel = QLabel("Zona actual: UTC")
        self.currentTimezoneLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.currentTimezoneLabel)

        buttonLayout = QHBoxLayout()
        self.previousButton = QPushButton("Anterior")
        self.nextButton = QPushButton("Siguiente")
        buttonLayout.addWidget(self.previousButton)
        buttonLayout.addWidget(self.nextButton)

        mainLayout.addLayout(buttonLayout)

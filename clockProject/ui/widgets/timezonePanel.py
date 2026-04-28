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
        mainLayout.setSpacing(12)

        self.currentCityLabel = QLabel("Ciudad: Bogotá")
        self.currentTimezoneLabel = QLabel("Zona horaria: America/Bogota")
        self.currentTimeLabel = QLabel("Hora local: 00:00:00")

        for label in (self.currentCityLabel, self.currentTimezoneLabel, self.currentTimeLabel):
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.currentCityLabel.setStyleSheet("font-size: 18px; font-weight: 700;")
        self.currentTimezoneLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.currentTimeLabel.setStyleSheet("font-size: 16px;")

        mainLayout.addWidget(self.currentCityLabel)
        mainLayout.addWidget(self.currentTimezoneLabel)
        mainLayout.addWidget(self.currentTimeLabel)

        buttonLayout = QHBoxLayout()
        self.previousButton = QPushButton("Anterior")
        self.nextButton = QPushButton("Siguiente")
        buttonLayout.addWidget(self.previousButton)
        buttonLayout.addWidget(self.nextButton)

        mainLayout.addLayout(buttonLayout)

    def updateTimezoneInfo(self, cityName: str, timezoneCode: str, timeText: str) -> None:
        """Update the visible timezone information."""
        self.currentCityLabel.setText(f"Ciudad: {cityName}")
        self.currentTimezoneLabel.setText(f"Zona horaria: {timezoneCode}")
        self.currentTimeLabel.setText(f"Hora local: {timeText}")

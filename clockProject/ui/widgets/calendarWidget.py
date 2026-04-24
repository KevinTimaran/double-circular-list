"""Calendar/date widget."""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class CalendarWidget(QWidget):
    """Displays current date in Spanish-friendly format."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.currentDateTime = datetime.now()
        self._buildUi()

    def _buildUi(self) -> None:
        layout = QVBoxLayout(self)
        self.dateLabel = QLabel("Fecha")
        self.dateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.dateLabel)
        self.updateDate(self.currentDateTime)

    def updateDate(self, dateTimeValue: datetime) -> None:
        """Update date label value."""
        self.currentDateTime = dateTimeValue
        self.dateLabel.setText(dateTimeValue.strftime("%d/%m/%Y"))

"""Calendar/date widget."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class CalendarWidget(QWidget):
    """Displays current date in Spanish-friendly format."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._buildUi()

    def _buildUi(self) -> None:
        layout = QVBoxLayout(self)
        self.dateLabel = QLabel("Fecha")
        self.dateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.dateLabel)

    def updateDate(self, dateText: str) -> None:
        """Update date label value."""
        self.dateLabel.setText(dateText)

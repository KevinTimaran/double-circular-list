"""Digital clock widget."""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DigitalClockWidget(QWidget):
    """Displays digital time text."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.currentDateTime = datetime.now()
        self._buildUi()

    def _buildUi(self) -> None:
        layout = QVBoxLayout(self)
        self.timeLabel = QLabel("00:00:00")
        self.timeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timeLabel)

    def setDateTime(self, dateTimeValue: datetime) -> None:
        """Update digital display from date/time value."""
        self.currentDateTime = dateTimeValue
        self.timeLabel.setText(dateTimeValue.strftime("%H:%M:%S"))

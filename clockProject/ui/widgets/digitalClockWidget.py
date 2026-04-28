"""Digital clock widget."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DigitalClockWidget(QWidget):
    """Displays digital time text."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._buildUi()

    def _buildUi(self) -> None:
        layout = QVBoxLayout(self)
        self.timeLabel = QLabel("00:00:00")
        self.timeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timeLabel)

    def updateTime(self, timeText: str) -> None:
        """Update the digital display with already formatted time text."""
        self.timeLabel.setText(timeText)

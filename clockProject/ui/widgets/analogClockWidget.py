"""Analog clock widget placeholder."""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AnalogClockWidget(QWidget):
    """Displays a placeholder for the analog clock."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.currentDateTime = datetime.now()
        self._buildUi()

    def _buildUi(self) -> None:
        layout = QVBoxLayout(self)
        self.placeholderLabel = QLabel("Reloj analógico (pendiente)")
        self.placeholderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.placeholderLabel)

    def setDateTime(self, dateTimeValue: datetime) -> None:
        """Update the displayed date/time reference."""
        self.currentDateTime = dateTimeValue
        self.placeholderLabel.setText(f"Reloj analógico: {dateTimeValue.strftime('%H:%M:%S')}")

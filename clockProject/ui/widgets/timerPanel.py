"""Countdown timer panel widget."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class TimerPanel(QWidget):
    """Provides base UI controls for the countdown timer."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._buildUi()

    def _buildUi(self) -> None:
        mainLayout = QVBoxLayout(self)

        self.timeLabel = QLabel("00:00")
        self.timeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.timeLabel)

        inputLayout = QHBoxLayout()
        self.minutesInput = QSpinBox()
        self.minutesInput.setRange(0, 999)
        self.minutesInput.setPrefix("Min: ")
        inputLayout.addWidget(self.minutesInput)
        mainLayout.addLayout(inputLayout)

        buttonLayout = QHBoxLayout()
        self.startButton = QPushButton("Iniciar")
        self.pauseButton = QPushButton("Pausar")
        self.resumeButton = QPushButton("Reanudar")
        self.resetButton = QPushButton("Reiniciar")

        buttonLayout.addWidget(self.startButton)
        buttonLayout.addWidget(self.pauseButton)
        buttonLayout.addWidget(self.resumeButton)
        buttonLayout.addWidget(self.resetButton)

        mainLayout.addLayout(buttonLayout)

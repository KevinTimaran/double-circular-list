"""Stopwatch panel widget."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class StopwatchPanel(QWidget):
    """Provides base UI controls for stopwatch interactions."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._buildUi()

    def _buildUi(self) -> None:
        mainLayout = QVBoxLayout(self)

        self.timeLabel = QLabel("00:00:00.00")
        self.timeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.timeLabel)

        controlsLayout = QGridLayout()
        self.startButton = QPushButton("Iniciar")
        self.pauseButton = QPushButton("Pausar")
        self.resumeButton = QPushButton("Reanudar")
        self.resetButton = QPushButton("Reiniciar")
        self.lapButton = QPushButton("Guardar vuelta")

        controlsLayout.addWidget(self.startButton, 0, 0)
        controlsLayout.addWidget(self.pauseButton, 0, 1)
        controlsLayout.addWidget(self.resumeButton, 1, 0)
        controlsLayout.addWidget(self.resetButton, 1, 1)
        controlsLayout.addWidget(self.lapButton, 2, 0, 1, 2)

        mainLayout.addLayout(controlsLayout)

        self.lapListWidget = QListWidget()
        self.lapListWidget.addItem("Historial de vueltas")
        mainLayout.addWidget(self.lapListWidget)

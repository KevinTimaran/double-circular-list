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

        # Small digital label (secondary) - main display is the analog clock
        self.smallTimeLabel = QLabel("00:00:00.00")
        self.smallTimeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.smallTimeLabel.font()
        font.setPointSize(max(10, font.pointSize() - 2))
        self.smallTimeLabel.setFont(font)
        mainLayout.addWidget(self.smallTimeLabel)

        controlsLayout = QGridLayout()
        self.startButton = QPushButton("Iniciar")
        self.pauseButton = QPushButton("Pausar")
        self.resumeButton = QPushButton("Reanudar")
        self.resetButton = QPushButton("Reiniciar")
        self.lapButton = QPushButton("Guardar vuelta")
        self.deleteButton = QPushButton("Borrar vuelta")
        self.previousButton = QPushButton("Anterior")
        self.nextButton = QPushButton("Siguiente")

        controlsLayout.addWidget(self.startButton, 0, 0)
        controlsLayout.addWidget(self.pauseButton, 0, 1)
        controlsLayout.addWidget(self.resumeButton, 1, 0)
        controlsLayout.addWidget(self.resetButton, 1, 1)
        controlsLayout.addWidget(self.lapButton, 2, 0, 1, 2)
        controlsLayout.addWidget(self.deleteButton, 3, 0, 1, 2)
        controlsLayout.addWidget(self.previousButton, 4, 0)
        controlsLayout.addWidget(self.nextButton, 4, 1)

        mainLayout.addLayout(controlsLayout)

        self.lapListWidget = QListWidget()
        self.lapListWidget.addItem("Sin vueltas registradas")
        mainLayout.addWidget(self.lapListWidget)

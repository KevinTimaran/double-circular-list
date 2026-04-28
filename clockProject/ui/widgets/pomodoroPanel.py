"""Pomodoro panel widget."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class PomodoroPanel(QWidget):
    """Provides UI controls for the Pomodoro timer."""

    settingsChanged = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._buildUi()

    def _buildUi(self) -> None:
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(16)
        mainLayout.setContentsMargins(16, 16, 16, 16)

        # Phase Info
        self.phaseLabel = QLabel("Fase actual")
        self.phaseLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phaseLabel.setStyleSheet("font-size: 20px; font-weight: bold; color: #f4f4f5;")
        mainLayout.addWidget(self.phaseLabel)

        self.digitalTimeLabel = QLabel("25:00")
        self.digitalTimeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.digitalTimeLabel.setStyleSheet("font-size: 48px; font-weight: bold; color: #3b82f6;")
        mainLayout.addWidget(self.digitalTimeLabel)

        self.completedLabel = QLabel("Completados: 0")
        self.completedLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.completedLabel.setStyleSheet("font-size: 14px; color: #a1a1aa;")
        mainLayout.addWidget(self.completedLabel)

        mainLayout.addStretch()

        # Settings
        settingsLayout = QHBoxLayout()
        settingsLayout.setSpacing(16)

        # Focus SpinBox
        self.focusSpinBox = QSpinBox()
        self.focusSpinBox.setRange(1, 60)
        self.focusSpinBox.setValue(25)
        focusForm = QFormLayout()
        focusForm.addRow("Enfoque (min):", self.focusSpinBox)

        # Short Break SpinBox
        self.shortBreakSpinBox = QSpinBox()
        self.shortBreakSpinBox.setRange(1, 30)
        self.shortBreakSpinBox.setValue(5)
        shortBreakForm = QFormLayout()
        shortBreakForm.addRow("Descanso Corto:", self.shortBreakSpinBox)

        # Long Break SpinBox
        self.longBreakSpinBox = QSpinBox()
        self.longBreakSpinBox.setRange(1, 60)
        self.longBreakSpinBox.setValue(15)
        longBreakForm = QFormLayout()
        longBreakForm.addRow("Descanso Largo:", self.longBreakSpinBox)

        settingsLayout.addLayout(focusForm)
        settingsLayout.addLayout(shortBreakForm)
        settingsLayout.addLayout(longBreakForm)

        mainLayout.addLayout(settingsLayout)
        mainLayout.addSpacing(12)

        # Controls
        controlsLayout = QHBoxLayout()
        controlsLayout.setSpacing(12)

        self.toggleButton = QPushButton("Iniciar")
        self.toggleButton.setMinimumHeight(44)
        
        self.skipButton = QPushButton("Omitir Fase")
        self.skipButton.setMinimumHeight(44)
        
        self.resetButton = QPushButton("Reiniciar Ciclo")
        self.resetButton.setMinimumHeight(44)

        controlsLayout.addWidget(self.toggleButton, stretch=2)
        controlsLayout.addWidget(self.skipButton, stretch=1)
        controlsLayout.addWidget(self.resetButton, stretch=1)

        mainLayout.addLayout(controlsLayout)

        self._connectSignals()

    def _connectSignals(self) -> None:
        self.focusSpinBox.valueChanged.connect(lambda _: self.settingsChanged.emit())
        self.shortBreakSpinBox.valueChanged.connect(lambda _: self.settingsChanged.emit())
        self.longBreakSpinBox.valueChanged.connect(lambda _: self.settingsChanged.emit())

    def getDurations(self) -> tuple[int, int, int]:
        """Return (focusMin, shortBreakMin, longBreakMin)"""
        return (
            self.focusSpinBox.value(),
            self.shortBreakSpinBox.value(),
            self.longBreakSpinBox.value(),
        )

    def updateDisplay(
        self,
        phaseName: str,
        timeText: str,
        completedCount: int,
        isRunning: bool,
        phaseColor: str
    ) -> None:
        """Refresh panel UI based on service state."""
        self.phaseLabel.setText(phaseName)
        self.digitalTimeLabel.setText(timeText)
        self.digitalTimeLabel.setStyleSheet(f"font-size: 48px; font-weight: bold; color: {phaseColor};")
        
        tomatoes = "🍅" * completedCount
        self.completedLabel.setText(f"Completados: {completedCount}  {tomatoes}")

        if isRunning:
            self.toggleButton.setText("Pausar")
        else:
            self.toggleButton.setText("Iniciar")

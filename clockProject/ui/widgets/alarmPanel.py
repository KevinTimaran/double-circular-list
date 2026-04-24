"""Alarm panel widget."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AlarmPanel(QWidget):
    """Provides the base alarm management panel UI."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._buildUi()

    def _buildUi(self) -> None:
        mainLayout = QVBoxLayout(self)

        self.alarmListWidget = QListWidget()
        self.alarmListWidget.addItem("Sin alarmas configuradas")
        mainLayout.addWidget(self.alarmListWidget)

        buttonLayout = QHBoxLayout()
        self.addButton = QPushButton("Agregar")
        self.editButton = QPushButton("Editar")
        self.removeButton = QPushButton("Eliminar")

        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.editButton)
        buttonLayout.addWidget(self.removeButton)

        mainLayout.addLayout(buttonLayout)

"""Alarm panel widget."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from models.alarm import Alarm


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
        self.toggleButton = QPushButton("Activar/Desactivar")
        self.previousButton = QPushButton("Anterior")
        self.nextButton = QPushButton("Siguiente")

        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.editButton)
        buttonLayout.addWidget(self.removeButton)
        buttonLayout.addWidget(self.toggleButton)
        buttonLayout.addWidget(self.previousButton)
        buttonLayout.addWidget(self.nextButton)

        mainLayout.addLayout(buttonLayout)

    def setAlarms(self, alarms: list[Alarm], selectedAlarmId: int | None = None) -> None:
        """Refresh the visual list with the current alarms."""
        self.alarmListWidget.clear()

        if not alarms:
            self.alarmListWidget.addItem("Sin alarmas configuradas")
            return

        for alarm in alarms:
            stateText = "Activa" if alarm.enabled else "Inactiva"
            itemText = f"{alarm.getDisplayTime()} - {alarm.label or 'Sin etiqueta'} ({stateText})"
            item = QListWidgetItem(itemText)
            item.setData(Qt.ItemDataRole.UserRole, alarm.alarmId)
            item.setForeground(QBrush(QColor("#166534") if alarm.enabled else QColor("#991b1b")))
            self.alarmListWidget.addItem(item)

        if selectedAlarmId is not None:
            self.selectAlarmById(alarms, selectedAlarmId)

    def getSelectedRow(self) -> int:
        """Return the selected row in the alarm list."""
        return self.alarmListWidget.currentRow()

    def getSelectedAlarmId(self, alarms: list[Alarm]) -> int | None:
        """Return the alarm id for the selected row."""
        currentItem = self.alarmListWidget.currentItem()
        if currentItem is None:
            return None
        alarmId = currentItem.data(Qt.ItemDataRole.UserRole)
        return alarmId if isinstance(alarmId, int) else None

    def selectAlarmById(self, alarms: list[Alarm], alarmId: int) -> None:
        """Select the row associated with the given alarm id."""
        for index, alarm in enumerate(alarms):
            if alarm.alarmId == alarmId:
                self.alarmListWidget.setCurrentRow(index)
                return

    def highlightCurrentAlarm(self) -> None:
        """Keep the current row visible and focused."""
        currentItem = self.alarmListWidget.currentItem()
        if currentItem is not None:
            currentItem.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

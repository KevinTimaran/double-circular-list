"""Dialog for creating or editing alarms."""

from __future__ import annotations

from datetime import time

from PySide6.QtCore import QTime
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QTimeEdit,
    QVBoxLayout,
)


class AlarmDialog(QDialog):
    """Base dialog used to collect alarm information."""

    def __init__(self, parent: QDialog | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Configurar alarma")
        self._buildUi()

    def _buildUi(self) -> None:
        mainLayout = QVBoxLayout(self)
        formLayout = QFormLayout()

        self.labelInput = QLineEdit()
        self.timeInput = QTimeEdit()
        self.timeInput.setDisplayFormat("HH:mm")
        self.timeInput.setTime(QTime.currentTime())
        self.repeatDailyCheckBox = QCheckBox("Repetir diariamente")

        formLayout.addRow("Etiqueta:", self.labelInput)
        formLayout.addRow("Hora:", self.timeInput)
        formLayout.addRow("Repetición:", self.repeatDailyCheckBox)

        mainLayout.addLayout(formLayout)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        mainLayout.addWidget(self.buttonBox)

    def getAlarmData(self) -> tuple[str, time, bool]:
        """Return user input data from dialog fields."""
        qtTime = self.timeInput.time()
        alarmTime = time(hour=qtTime.hour(), minute=qtTime.minute())
        return self.labelInput.text().strip(), alarmTime, self.repeatDailyCheckBox.isChecked()

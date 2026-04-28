"""Dialog for creating or editing alarms."""

from __future__ import annotations

from PySide6.QtCore import QTime
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QTimeEdit,
    QVBoxLayout,
)


class AlarmDialog(QDialog):
    """Base dialog used to collect alarm information."""

    def __init__(self, parent: QDialog | None = None, alarmData: dict | None = None) -> None:
        super().__init__(parent)
        self._alarmData = alarmData or {}
        self.setWindowTitle("Editar alarma" if self._alarmData else "Configurar alarma")
        self._buildUi()
        self._loadInitialData()

    def _buildUi(self) -> None:
        mainLayout = QVBoxLayout(self)
        formLayout = QFormLayout()

        self.labelInput = QLineEdit()
        self.timeInput = QTimeEdit()
        self.timeInput.setDisplayFormat("hh:mm AP")
        self.timeInput.setTime(QTime.currentTime())
        self.activeCheckBox = QCheckBox("Activa")
        self.activeCheckBox.setChecked(True)

        formLayout.addRow("Etiqueta:", self.labelInput)
        formLayout.addRow("Hora:", self.timeInput)
        formLayout.addRow("Estado:", self.activeCheckBox)

        mainLayout.addLayout(formLayout)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        mainLayout.addWidget(self.buttonBox)

    def _loadInitialData(self) -> None:
        """Populate the dialog when editing an existing alarm."""
        if not self._alarmData:
            return

        self.labelInput.setText(str(self._alarmData.get("label", "")))
        hour = int(self._alarmData.get("hour", QTime.currentTime().hour()))
        minute = int(self._alarmData.get("minute", QTime.currentTime().minute()))
        self.timeInput.setTime(QTime(hour, minute))
        self.activeCheckBox.setChecked(bool(self._alarmData.get("enabled", True)))

    def validateInputs(self) -> bool:
        """Validate the dialog inputs before saving."""
        hour = self.timeInput.time().hour()
        minute = self.timeInput.time().minute()

        if hour < 0 or hour > 23:
            return False
        if minute < 0 or minute > 59:
            return False
        return True

    def getAlarmData(self) -> dict:
        """Return user input data from dialog fields."""
        qtTime = self.timeInput.time()
        return {
            "hour": qtTime.hour(),
            "minute": qtTime.minute(),
            "label": self.labelInput.text().strip(),
            "enabled": self.activeCheckBox.isChecked(),
        }

    def accept(self) -> None:
        """Validate input before closing the dialog."""
        if not self.validateInputs():
            QMessageBox.warning(
                self,
                "Entrada inválida",
                "Por favor, verifica la hora (00:00 a 23:59).",
            )
            return
        super().accept()

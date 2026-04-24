"""Dialog for manual date/time selection."""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import (
    QCheckBox,
    QDateTimeEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QVBoxLayout,
)


class ManualTimeDialog(QDialog):
    """Base dialog to configure automatic or manual clock mode."""

    def __init__(self, parent: QDialog | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Editar hora y fecha")
        self._buildUi()

    def _buildUi(self) -> None:
        mainLayout = QVBoxLayout(self)
        formLayout = QFormLayout()

        self.automaticModeCheckBox = QCheckBox("Usar hora automática del sistema")
        self.automaticModeCheckBox.setChecked(True)

        self.dateTimeInput = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateTimeInput.setDisplayFormat("dd/MM/yyyy HH:mm:ss")

        formLayout.addRow("Modo:", self.automaticModeCheckBox)
        formLayout.addRow("Fecha y hora manual:", self.dateTimeInput)

        mainLayout.addLayout(formLayout)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        mainLayout.addWidget(self.buttonBox)

    def getData(self) -> tuple[bool, datetime]:
        """Return selected mode and manual datetime value."""
        value = self.dateTimeInput.dateTime().toPython()
        return self.automaticModeCheckBox.isChecked(), value

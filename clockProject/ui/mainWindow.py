"""Main application window."""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGroupBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Signal

from ui.widgets.alarmPanel import AlarmPanel
from ui.widgets.analogClockWidget import AnalogClockWidget
from ui.widgets.calendarWidget import CalendarWidget
from ui.widgets.digitalClockWidget import DigitalClockWidget
from ui.widgets.pomodoroPanel import PomodoroPanel
from ui.widgets.settingsPanel import SettingsPanel
from ui.widgets.stopwatchPanel import StopwatchPanel
from ui.widgets.timezonePanel import TimezonePanel


class ClickableCard(QFrame):
    """A custom card widget that emits a clicked signal."""

    clicked = Signal()

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(110)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(128, 128, 128, 0.1);
                border-radius: 12px;
                border: 1px solid rgba(128, 128, 128, 0.2);
            }
            QFrame:hover {
                background-color: rgba(128, 128, 128, 0.2);
                border: 1px solid rgba(128, 128, 128, 0.4);
            }
        """)

        layout = QVBoxLayout(self)
        titleLabel = QLabel(title)
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titleLabel.setStyleSheet("font-weight: bold; font-size: 16px; background: transparent; border: none;")

        stateLabel = QLabel("Entrar →")
        stateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stateLabel.setStyleSheet("font-size: 13px; background: transparent; border: none; color: #a1a1aa;")

        layout.addStretch()
        layout.addWidget(titleLabel)
        layout.addSpacing(8)
        layout.addWidget(stateLabel)
        layout.addStretch()

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class MainWindow(QMainWindow):
    """Composes the high-level UI sections of the clock application."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Reloj Multifunción")
        self.resize(1200, 720)

        self._buildUi()

    def _buildUi(self) -> None:
        self.pages = QStackedWidget()
        self.homePage = self._createHomePage()
        self.clockPage = self._createClockPage()

        self.pages.addWidget(self.homePage)
        self.pages.addWidget(self.clockPage)

        self.setCentralWidget(self.pages)
        self.statusBar().showMessage("Aplicación inicializada")

    def _createHomePage(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(20)

        titleLabel = QLabel("Reloj Multifunción")
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titleLabel.setStyleSheet("font-size: 32px; font-weight: 700;")
        layout.addWidget(titleLabel)

        self.previewAnalogClockWidget = AnalogClockWidget(clickable=True)
        self.previewAnalogClockWidget.setMinimumSize(380, 380)
        self.previewAnalogClockWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.previewAnalogClockWidget, stretch=1)

        self.openClockButton = QPushButton("Abrir vista detallada")
        self.openClockButton.setMinimumHeight(46)
        self.openClockButton.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.openClockButton)

        placeholderGrid = QGridLayout()
        placeholderGrid.setSpacing(12)

        placeholderTitles = [
            "Pomodoro",
            "Alarmas",
            "Cronómetro",
            "Zona horaria",
            "Configuración",
        ]

        self.homeCards = {}
        for index, title in enumerate(placeholderTitles):
            card = ClickableCard(title)
            self.homeCards[title] = card
            placeholderGrid.addWidget(card, index // 3, index % 3)

        layout.addLayout(placeholderGrid)
        return page

    def _createClockPage(self) -> QWidget:
        page = QWidget()
        rootLayout = QVBoxLayout(page)
        rootLayout.setContentsMargins(24, 20, 24, 20)
        rootLayout.setSpacing(16)

        headerLayout = QHBoxLayout()
        titleLabel = QLabel("Reloj")
        titleLabel.setStyleSheet("font-size: 24px; font-weight: 700;")
        self.backButton = QPushButton("Volver")
        headerLayout.addWidget(titleLabel)
        headerLayout.addStretch()
        headerLayout.addWidget(self.backButton)
        rootLayout.addLayout(headerLayout)

        self.analogClockWidget = AnalogClockWidget()
        self.analogClockWidget.setMinimumSize(380, 380)
        self.analogClockWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.digitalClockWidget = DigitalClockWidget(page)
        self.calendarWidget = CalendarWidget(page)
        self.digitalClockWidget.hide()
        self.calendarWidget.hide()

        clockContainerLayout = QVBoxLayout()
        clockContainerLayout.addStretch()
        clockContainerLayout.addWidget(self.analogClockWidget, alignment=Qt.AlignmentFlag.AlignHCenter)
        clockContainerLayout.addStretch()
        rootLayout.addLayout(clockContainerLayout, stretch=2)

        self.tabs = QTabWidget()

        self.pomodoroPanel = PomodoroPanel()
        self.alarmPanel = AlarmPanel()
        self.stopwatchPanel = StopwatchPanel()
        self.timezonePanel = TimezonePanel()
        self.settingsPanel = SettingsPanel()

        self.tabs.addTab(self.pomodoroPanel, "Pomodoro")
        self.tabs.addTab(self.alarmPanel, "Alarmas")
        self.tabs.addTab(self.stopwatchPanel, "Cronómetro")
        self.tabs.addTab(self.timezonePanel, "Zona horaria")
        self.tabs.addTab(self.settingsPanel, "Configuración")

        rootLayout.addWidget(self.tabs, stretch=1)

        return page

    def _createGroupBox(self, title: str, contentWidget: QWidget) -> QGroupBox:
        """Create a titled section with the provided content widget."""
        groupBox = QGroupBox(title)
        layout = QVBoxLayout(groupBox)
        layout.addWidget(contentWidget)
        return groupBox

    def showHomePage(self) -> None:
        """Show the home page."""
        self.pages.setCurrentWidget(self.homePage)

    def showClockPage(self) -> None:
        """Show the dedicated clock page."""
        self.pages.setCurrentWidget(self.clockPage)

    def navigateToTab(self, index: int) -> None:
        """Navigate directly to a specific tab on the clock page."""
        self.tabs.setCurrentIndex(index)
        self.showClockPage()

    def updateDigitalClock(self, timeText: str) -> None:
        """Update the digital clock section."""
        self.digitalClockWidget.updateTime(timeText)

    def updateDateLabel(self, dateText: str) -> None:
        """Update the date section."""
        self.calendarWidget.updateDate(dateText)

    def updateAnalogClock(self, currentDateTime: datetime) -> None:
        """Update the analog clock section."""
        self.previewAnalogClockWidget.updateDateTime(currentDateTime)
        self.analogClockWidget.updateDateTime(currentDateTime)

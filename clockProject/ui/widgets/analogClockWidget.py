"""Analog clock widget."""

from __future__ import annotations

import math
from datetime import datetime
from typing import Optional

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import QWidget

from models.clockStyle import ClockStyle


class AnalogClockWidget(QWidget):
    """Displays an analog clock painted with PySide6."""

    clicked = Signal()

    WEEKDAY_LABELS = ("Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb")
    MONTH_LABELS = ("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")

    def __init__(self, parent: QWidget | None = None, clickable: bool = False) -> None:
        super().__init__(parent)
        self.currentDateTime = datetime.now()
        # displayMode: 'clock', 'stopwatch', or 'pomodoro'
        self._displayMode = "clock"
        self._stopwatchElapsedMs: int = 0
        
        self._pomodoroRemainingMs: int = 0
        self._pomodoroTotalMs: int = 1
        self._pomodoroColor: str = "#ef4444"
        
        self.clickable = clickable
        self.setMinimumSize(220, 220)
        self.clockStyle: Optional[ClockStyle] = None

        if self.clickable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)

    def setClockStyle(self, style: Optional[ClockStyle]) -> None:
        """Set the clock style to use for rendering."""
        self.clockStyle = style
        self.update()

    def updateDateTime(self, dateTimeValue: datetime) -> None:
        """Store the current date/time and schedule a repaint."""
        # Only update internal datetime in clock mode
        if self._displayMode == "clock":
            self.currentDateTime = dateTimeValue
        self.update()

    def paintEvent(self, event) -> None:
        """Paint the clock face, marks, numbers, and hands."""
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        side = min(self.width(), self.height())
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = side * 0.42

        self._drawOuterRing(painter, center, radius)
        self._drawClockFace(painter, center, radius)

        if self._displayMode == "clock":
            if self.clockStyle and self.clockStyle.showMinuteMarks:
                self._drawMinuteMarks(painter, center, radius)
            self._drawHourMarks(painter, center, radius)
            if self.clockStyle and self.clockStyle.showNumbers:
                self._drawNumbers(painter, center, radius)
            if self.clockStyle and self.clockStyle.showDateInfo:
                self._drawIntegratedDateInfo(painter, center, radius)
            self._drawHands(painter, center, radius)
        elif self._displayMode == "stopwatch":
            self._drawStopwatchDial(painter, center, radius)
            self._drawStopwatchHands(painter, center, radius)
            self._drawStopwatchDigital(painter, center, radius)
        elif self._displayMode == "pomodoro":
            self._drawClockFace(painter, center, radius)
            self._drawPomodoroArc(painter, center, radius)
            self._drawHourMarks(painter, center, radius)
            self._drawPomodoroHands(painter, center, radius)

        self._drawCenterCap(painter, center, radius)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Emit a click signal when the clock is pressed."""
        if self.clickable and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        super().mousePressEvent(event)

    def _drawOuterRing(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw the decorative outside rings of the clock."""
        painter.setBrush(Qt.BrushStyle.NoBrush)

        ringColor = self.clockStyle.ringColor if self.clockStyle else "#0f172a"
        painter.setPen(QPen(QColor(ringColor), max(3, int(radius * 0.045))))
        painter.drawEllipse(center, radius, radius)

        painter.setPen(QPen(QColor("#cbd5e1"), max(1, int(radius * 0.018))))
        painter.drawEllipse(center, radius * 0.93, radius * 0.93)

    def _drawClockFace(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw the inner clock face."""
        painter.setPen(Qt.PenStyle.NoPen)
        dialColor = self.clockStyle.dialBackground if self.clockStyle else "#f8fafc"
        painter.setBrush(QColor(dialColor))
        painter.drawEllipse(center, radius * 0.9, radius * 0.9)

    def _drawMinuteMarks(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw the small marks for each minute."""
        for minute in range(60):
            if minute % 5 == 0:
                continue

            angle = math.radians(minute * 6 - 90)
            outerPoint = self._pointOnCircle(center, radius * 0.83, angle)
            innerPoint = self._pointOnCircle(center, radius * 0.79, angle)
            markWidth = max(1, int(radius * 0.01))

            painter.setPen(QPen(QColor("#94a3b8"), markWidth, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawLine(innerPoint, outerPoint)

    def _drawHourMarks(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw the larger marks for each hour."""
        for hour in range(12):
            angle = math.radians(hour * 30 - 90)
            outerPoint = self._pointOnCircle(center, radius * 0.85, angle)
            innerPoint = self._pointOnCircle(center, radius * 0.75, angle)
            markWidth = max(2, int(radius * 0.028))

            ringColor = self.clockStyle.ringColor if self.clockStyle else "#0f172a"
            painter.setPen(QPen(QColor(ringColor), markWidth, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawLine(innerPoint, outerPoint)

    def _drawNumbers(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw numbers from 1 to 12."""
        font = QFont()
        font.setPointSize(max(10, int(radius * 0.12)))
        font.setBold(True)
        painter.setFont(font)

        numberColor = self.clockStyle.numberColor if self.clockStyle else "#111827"
        painter.setPen(QColor(numberColor))

        numberBoxSize = radius * 0.24

        for number in range(1, 13):
            angle = math.radians(number * 30 - 90)
            point = self._pointOnCircle(center, radius * 0.6, angle)
            textRect = QRectF(
                point.x() - numberBoxSize / 2,
                point.y() - numberBoxSize / 2,
                numberBoxSize,
                numberBoxSize,
            )
            painter.drawText(textRect, Qt.AlignmentFlag.AlignCenter, str(number))

    def _drawIntegratedDateInfo(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw the date information integrated inside the dial."""
        weekdayText = self.WEEKDAY_LABELS[self.currentDateTime.weekday()]
        dayText = f"{self.currentDateTime.day:02d}"
        monthText = self.MONTH_LABELS[self.currentDateTime.month - 1].upper()
        monthNumberText = f"{self.currentDateTime.month:02d}"
        yearText = str(self.currentDateTime.year)

        painter.save()
        painter.setPen(QColor("#334155"))

        leftFont = QFont()
        leftFont.setBold(True)
        leftFont.setPointSize(max(9, int(radius * 0.075)))
        painter.setFont(leftFont)
        leftWidth = radius * 0.46
        leftHeight = radius * 0.15
        leftRect = QRectF(
            center.x() - radius * 0.47,
            center.y() - radius * 0.03,
            leftWidth,
            leftHeight,
        )
        self._drawCompactLabel(painter, leftRect, weekdayText, dayText, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        rightFont = QFont()
        rightFont.setBold(True)
        rightFont.setPointSize(max(9, int(radius * 0.075)))
        painter.setFont(rightFont)
        rightRect = QRectF(
            center.x() + radius * 0.01,
            center.y() - radius * 0.03,
            radius * 0.47,
            radius * 0.15,
        )
        self._drawCompactLabel(
            painter,
            rightRect,
            monthText,
            monthNumberText,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
        )

        yearFont = QFont()
        yearFont.setBold(True)
        yearFont.setPointSize(max(10, int(radius * 0.09)))
        painter.setFont(yearFont)
        yearRect = QRectF(
            center.x() - radius * 0.16,
            center.y() + radius * 0.34,
            radius * 0.32,
            radius * 0.1,
        )
        painter.setPen(QColor("#475569"))
        painter.drawText(yearRect, Qt.AlignmentFlag.AlignCenter, yearText)

        painter.restore()

    def _drawCompactLabel(self, painter: QPainter, rect: QRectF, primary: str, secondary: str, alignment: Qt.AlignmentFlag) -> None:
        """Draw a compact two-part date label inside a bounded area."""
        painter.drawText(rect, alignment, f"{primary}  {secondary}")

    def _drawHands(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw the hour, minute, and second hands."""
        hour = self.currentDateTime.hour % 12
        minute = self.currentDateTime.minute
        second = self.currentDateTime.second

        hourAngle = math.radians((hour + minute / 60) * 30 - 90)
        minuteAngle = math.radians((minute + second / 60) * 6 - 90)
        secondAngle = math.radians(second * 6 - 90)

        hourColor = self.clockStyle.hourHandColor if self.clockStyle else "#0f172a"
        minuteColor = self.clockStyle.minuteHandColor if self.clockStyle else "#1e293b"
        secondColor = self.clockStyle.secondHandColor if self.clockStyle else "#dc2626"

        self._drawHand(painter, center, radius * 0.38, hourAngle, hourColor, max(5, int(radius * 0.065)))
        self._drawHand(painter, center, radius * 0.6, minuteAngle, minuteColor, max(3, int(radius * 0.038)))

        if not self.clockStyle or self.clockStyle.showSeconds:
            self._drawHand(painter, center, radius * 0.72, secondAngle, secondColor, max(1, int(radius * 0.012)))
            secondTail = self._pointOnCircle(center, radius * 0.14, secondAngle + math.pi)
            painter.setPen(QPen(QColor(secondColor), max(1, int(radius * 0.012)), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawLine(center, secondTail)

    # -------------------------
    # Stopwatch drawing helpers
    # -------------------------
    def _drawStopwatchDial(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw a stopwatch-focused dial with prominent 60-second scale."""
        # Fine ticks (60)
        ringColor = self.clockStyle.ringColor if self.clockStyle else "#0f172a"
        for secondMark in range(60):
            angle = math.radians(secondMark * 6 - 90)
            outer = self._pointOnCircle(center, radius * 0.84, angle)
            if secondMark % 5 == 0:
                inner = self._pointOnCircle(center, radius * 0.73, angle)
                width = max(2, int(radius * 0.022))
                color = QColor(ringColor)
            else:
                inner = self._pointOnCircle(center, radius * 0.78, angle)
                width = max(1, int(radius * 0.009))
                color = QColor("#64748b")

            painter.setPen(QPen(color, width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawLine(inner, outer)

        # Stopwatch numeric scale in tens: 60 at top, then 10..50 clockwise
        font = QFont()
        font.setPointSize(max(9, int(radius * 0.1)))
        font.setBold(True)
        painter.setFont(font)

        numberColor = self.clockStyle.numberColor if self.clockStyle else "#111827"
        painter.setPen(QColor(numberColor))

        numberBoxSize = radius * 0.24
        labels = {0: "60", 2: "10", 4: "20", 6: "30", 8: "40", 10: "50"}
        for hourIndex, label in labels.items():
            angle = math.radians(hourIndex * 30 - 90)
            point = self._pointOnCircle(center, radius * 0.59, angle)
            textRect = QRectF(
                point.x() - numberBoxSize / 2,
                point.y() - numberBoxSize / 2,
                numberBoxSize,
                numberBoxSize,
            )
            painter.drawText(textRect, Qt.AlignmentFlag.AlignCenter, label)

        # Subtle stopwatch title near the top center
        titleFont = QFont()
        titleFont.setPointSize(max(7, int(radius * 0.055)))
        titleFont.setBold(True)
        painter.setFont(titleFont)
        painter.setPen(QColor("#475569"))
        titleRect = QRectF(center.x() - radius * 0.25, center.y() - radius * 0.40, radius * 0.5, radius * 0.08)
        painter.drawText(titleRect, Qt.AlignmentFlag.AlignCenter, "CRONÓMETRO")

    def _drawStopwatchHands(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw hands based on elapsed milliseconds for stopwatch mode."""
        total_seconds = (self._stopwatchElapsedMs or 0) / 1000.0
        seconds = total_seconds % 60
        minutes = (total_seconds // 60) % 60
        hours = total_seconds // 3600

        secondAngle = math.radians(seconds * 6 - 90)
        minuteAngle = math.radians((minutes + seconds / 60.0) * 6 - 90)
        hourAngle = math.radians((hours % 12 + minutes / 60.0) * 30 - 90)

        hourColor = self.clockStyle.hourHandColor if self.clockStyle else "#0f172a"
        minuteColor = self.clockStyle.minuteHandColor if self.clockStyle else "#1e293b"
        secondColor = self.clockStyle.secondHandColor if self.clockStyle else "#dc2626"

        # Hour hand (elapsed hours)
        self._drawHand(painter, center, radius * 0.34, hourAngle, hourColor, max(5, int(radius * 0.065)))
        # Minute hand (elapsed minutes)
        self._drawHand(painter, center, radius * 0.56, minuteAngle, minuteColor, max(3, int(radius * 0.04)))
        # Second hand (elapsed seconds)
        self._drawHand(painter, center, radius * 0.78, secondAngle, secondColor, max(1, int(radius * 0.011)))

        # tail for second hand
        secondTail = self._pointOnCircle(center, radius * 0.14, secondAngle + math.pi)
        painter.setPen(QPen(QColor(secondColor), max(1, int(radius * 0.012)), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(center, secondTail)

    def _drawStopwatchDigital(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw a small digital elapsed time inside the clock center for convenience."""
        total_ms = int(self._stopwatchElapsedMs or 0)
        cs = int((total_ms % 1000) / 10)
        total_seconds = total_ms // 1000
        secs = total_seconds % 60
        mins = (total_seconds // 60) % 60
        hours = total_seconds // 3600
        text = f"{hours:02d}:{mins:02d}:{secs:02d}.{cs:02d}"

        font = QFont()
        font.setPointSize(max(7, int(radius * 0.075)))
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(QColor("#334155"))
        digitalRect = QRectF(center.x() - radius * 0.46, center.y() + radius * 0.20, radius * 0.92, radius * 0.14)
        painter.drawText(digitalRect, Qt.AlignmentFlag.AlignCenter, text)

    def _drawHand(
        self,
        painter: QPainter,
        center: QPointF,
        length: float,
        angle: float,
        color: str,
        width: int,
    ) -> None:
        """Draw one clock hand from the center to the selected angle."""
        endPoint = self._pointOnCircle(center, length, angle)
        painter.setPen(QPen(QColor(color), width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(center, endPoint)

    def _drawCenterCap(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw the center cap over the hands."""
        ringColor = self.clockStyle.ringColor if self.clockStyle else "#0f172a"
        painter.setPen(QPen(QColor("#f8fafc"), max(1, int(radius * 0.015))))
        painter.setBrush(QColor(ringColor))
        painter.drawEllipse(center, radius * 0.07, radius * 0.07)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#dc2626"))
        painter.drawEllipse(center, radius * 0.035, radius * 0.035)

    def _pointOnCircle(self, center: QPointF, radius: float, angle: float) -> QPointF:
        """Return a point placed on a circle for the given angle."""
        x = center.x() + math.cos(angle) * radius
        y = center.y() + math.sin(angle) * radius
        return QPointF(x, y)

    # -------------------------
    # Pomodoro drawing helpers
    # -------------------------
    def _drawPomodoroArc(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw a shrinking colored arc representing the remaining time."""
        if self._pomodoroTotalMs <= 0:
            return

        ratio = self._pomodoroRemainingMs / self._pomodoroTotalMs
        ratio = max(0.0, min(1.0, ratio))

        painter.setPen(Qt.PenStyle.NoPen)
        color = QColor(self._pomodoroColor)
        color.setAlpha(180)
        painter.setBrush(color)

        arcRadius = radius * 0.88
        rect = QRectF(center.x() - arcRadius, center.y() - arcRadius, arcRadius * 2, arcRadius * 2)

        startAngle = 90 * 16  # 12 o'clock in 1/16th of a degree
        spanAngle = int(-360 * ratio * 16)  # Negative draws clockwise

        painter.drawPie(rect, startAngle, spanAngle)

    def _drawPomodoroHands(self, painter: QPainter, center: QPointF, radius: float) -> None:
        """Draw hands representing the remaining minutes and seconds."""
        total_seconds = max(0, self._pomodoroRemainingMs / 1000.0)
        minutes = total_seconds / 60.0
        seconds = total_seconds % 60.0

        minuteAngle = math.radians(minutes * 6 - 90)
        secondAngle = math.radians(seconds * 6 - 90)

        minuteColor = self.clockStyle.minuteHandColor if self.clockStyle else "#1e293b"
        secondColor = self.clockStyle.secondHandColor if self.clockStyle else "#dc2626"

        self._drawHand(painter, center, radius * 0.65, minuteAngle, minuteColor, max(4, int(radius * 0.05)))
        self._drawHand(painter, center, radius * 0.8, secondAngle, secondColor, max(1, int(radius * 0.015)))

        secondTail = self._pointOnCircle(center, radius * 0.14, secondAngle + math.pi)
        painter.setPen(QPen(QColor(secondColor), max(1, int(radius * 0.015)), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(center, secondTail)

    # -------------------------
    # Public API
    # -------------------------
    def setDisplayMode(self, mode: str) -> None:
        """Set display mode: 'clock', 'stopwatch', or 'pomodoro'."""
        if mode not in ("clock", "stopwatch", "pomodoro"):
            return
        self._displayMode = mode
        self.update()

    def updateStopwatchElapsedMilliseconds(self, value: int) -> None:
        """Update internal elapsed milliseconds for stopwatch rendering."""
        self._stopwatchElapsedMs = max(0, int(value or 0))
        self.update()

    def updatePomodoroState(self, remainingMs: int, totalMs: int, colorHex: str) -> None:
        """Update internal state for pomodoro rendering."""
        self._pomodoroRemainingMs = remainingMs
        self._pomodoroTotalMs = totalMs
        self._pomodoroColor = colorHex
        self.update()

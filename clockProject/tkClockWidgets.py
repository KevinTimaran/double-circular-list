"""Reusable Tkinter widgets for the multifunction clock application."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Callable

import tkinter as tk
from tkinter import ttk


@dataclass(frozen=True)
class ThemePalette:
    """Application theme colors."""

    name: str
    appBackground: str
    panelBackground: str
    surfaceBackground: str
    textColor: str
    mutedTextColor: str
    accentColor: str
    accentHoverColor: str
    borderColor: str


@dataclass(frozen=True)
class ClockStylePreset:
    """Analog clock style preset."""

    name: str
    dialBackground: str
    ringColor: str
    numberColor: str
    hourHandColor: str
    minuteHandColor: str
    secondHandColor: str
    showNumbers: bool = True
    showMinuteMarks: bool = True
    showDateInfo: bool = True


class HoverButton(ttk.Button):
    """A ttk button with lightweight hover styling."""

    def __init__(
        self,
        master: tk.Misc,
        *,
        normalStyle: str,
        hoverStyle: str,
        **kwargs,
    ) -> None:
        super().__init__(master, style=normalStyle, **kwargs)
        self.normalStyle = normalStyle
        self.hoverStyle = hoverStyle
        self.bind("<Enter>", self._onEnter)
        self.bind("<Leave>", self._onLeave)

    def _onEnter(self, _event: tk.Event) -> None:
        self.configure(style=self.hoverStyle)

    def _onLeave(self, _event: tk.Event) -> None:
        self.configure(style=self.normalStyle)


class NavigationCard(ttk.Frame):
    """Clickable navigation card used on the home screen."""

    def __init__(
        self,
        master: tk.Misc,
        title: str,
        subtitle: str,
        emoji: str,
        command: Callable[[], None],
        *,
        stylePrefix: str,
    ) -> None:
        super().__init__(master, style=f"{stylePrefix}.Card.TFrame", padding=18)
        self.command = command
        self.normalStyle = f"{stylePrefix}.Card.TFrame"
        self.hoverStyle = f"{stylePrefix}.CardHover.TFrame"
        self.configure(cursor="hand2")

        self.columnconfigure(1, weight=1)

        self.emojiLabel = ttk.Label(self, text=emoji, style=f"{stylePrefix}.CardEmoji.TLabel")
        self.emojiLabel.grid(row=0, column=0, rowspan=2, sticky="n", padx=(0, 14))

        self.titleLabel = ttk.Label(self, text=title, style=f"{stylePrefix}.CardTitle.TLabel")
        self.titleLabel.grid(row=0, column=1, sticky="w")

        self.subtitleLabel = ttk.Label(self, text=subtitle, style=f"{stylePrefix}.CardSubtitle.TLabel")
        self.subtitleLabel.grid(row=1, column=1, sticky="w", pady=(4, 0))

        self.arrowLabel = ttk.Label(self, text="›", style=f"{stylePrefix}.CardArrow.TLabel")
        self.arrowLabel.grid(row=0, column=2, rowspan=2, sticky="e", padx=(14, 0))

        for widget in (self, self.emojiLabel, self.titleLabel, self.subtitleLabel, self.arrowLabel):
            widget.bind("<Enter>", self._onEnter)
            widget.bind("<Leave>", self._onLeave)
            widget.bind("<Button-1>", self._onClick)

    def _onEnter(self, _event: tk.Event) -> None:
        self.configure(style=self.hoverStyle)

    def _onLeave(self, _event: tk.Event) -> None:
        self.configure(style=self.normalStyle)

    def _onClick(self, _event: tk.Event) -> None:
        self.command()


class AnalogClockCanvas(tk.Canvas):
    """Responsive analog clock drawn with Tkinter canvas primitives."""

    def __init__(
        self,
        master: tk.Misc,
        *,
        theme: ThemePalette,
        style: ClockStylePreset,
        showSeconds: bool = True,
        showDateInfo: bool = True,
        diameter: int = 360,
    ) -> None:
        super().__init__(
            master,
            width=diameter,
            height=diameter,
            highlightthickness=0,
            bd=0,
            relief="flat",
            bg=theme.surfaceBackground,
        )
        self.theme = theme
        self.style = style
        self.showSeconds = showSeconds
        self.showDateInfo = showDateInfo
        self.currentDateTime = datetime.now()
        self._lastDrawnSize = (0, 0)
        self.bind("<Configure>", self._onResize)

    def setTheme(self, theme: ThemePalette) -> None:
        """Update the clock background theme."""
        self.theme = theme
        self.configure(bg=theme.surfaceBackground)
        self.redraw()

    def setStyle(self, style: ClockStylePreset) -> None:
        """Update the clock style preset."""
        self.style = style
        self.redraw()

    def setShowSeconds(self, value: bool) -> None:
        """Toggle the second hand visibility."""
        self.showSeconds = value
        self.redraw()

    def setShowDateInfo(self, value: bool) -> None:
        """Toggle the integrated date label."""
        self.showDateInfo = value
        self.redraw()

    def updateTime(self, dateTimeValue: datetime) -> None:
        """Store the current time and redraw the clock."""
        self.currentDateTime = dateTimeValue
        self.redraw()

    def redraw(self) -> None:
        """Redraw the entire clock face."""
        self.delete("all")

        width = max(1, self.winfo_width())
        height = max(1, self.winfo_height())
        if (width, height) == (1, 1):
            width = int(self.cget("width"))
            height = int(self.cget("height"))

        self._lastDrawnSize = (width, height)
        size = min(width, height)
        centerX = width / 2
        centerY = height / 2
        radius = size * 0.42

        self._drawShadow(centerX, centerY, radius)
        self._drawDial(centerX, centerY, radius)
        self._drawMarks(centerX, centerY, radius)
        self._drawNumbers(centerX, centerY, radius)
        self._drawHands(centerX, centerY, radius)
        self._drawCenterCap(centerX, centerY, radius)
        if self.showDateInfo:
            self._drawDateInfo(centerX, centerY, radius)

    def _onResize(self, _event: tk.Event) -> None:
        """Redraw the clock when the canvas size changes."""
        self.redraw()

    def _drawShadow(self, centerX: float, centerY: float, radius: float) -> None:
        """Draw a subtle shadow behind the clock."""
        self.create_oval(
            centerX - radius - 10,
            centerY - radius - 6,
            centerX + radius + 10,
            centerY + radius + 10,
            fill="#050814",
            outline="",
        )

    def _drawDial(self, centerX: float, centerY: float, radius: float) -> None:
        """Draw the outer ring and dial background."""
        self.create_oval(
            centerX - radius,
            centerY - radius,
            centerX + radius,
            centerY + radius,
            fill=self.style.ringColor,
            outline="",
        )
        self.create_oval(
            centerX - radius * 0.94,
            centerY - radius * 0.94,
            centerX + radius * 0.94,
            centerY + radius * 0.94,
            fill=self.style.dialBackground,
            outline="",
        )
        self.create_oval(
            centerX - radius * 0.88,
            centerY - radius * 0.88,
            centerX + radius * 0.88,
            centerY + radius * 0.88,
            fill=self.style.dialBackground,
            outline="#25314f",
            width=2,
        )

    def _drawMarks(self, centerX: float, centerY: float, radius: float) -> None:
        """Draw minute and hour marks."""
        for minute in range(60):
            angle = math.radians(minute * 6 - 90)
            outerX = centerX + math.cos(angle) * radius * 0.80
            outerY = centerY + math.sin(angle) * radius * 0.80
            if minute % 5 == 0:
                innerRadius = radius * 0.70
                width = max(2, int(radius * 0.018))
            else:
                if not self.style.showMinuteMarks:
                    continue
                innerRadius = radius * 0.75
                width = max(1, int(radius * 0.009))

            innerX = centerX + math.cos(angle) * innerRadius
            innerY = centerY + math.sin(angle) * innerRadius
            self.create_line(
                innerX,
                innerY,
                outerX,
                outerY,
                fill=self.style.ringColor if minute % 5 == 0 else self.theme.mutedTextColor,
                width=width,
                capstyle=tk.ROUND,
            )

    def _drawNumbers(self, centerX: float, centerY: float, radius: float) -> None:
        """Draw hour numbers around the dial."""
        if not self.style.showNumbers:
            return

        fontSize = max(11, int(radius * 0.13))
        for number in range(1, 13):
            angle = math.radians(number * 30 - 90)
            x = centerX + math.cos(angle) * radius * 0.58
            y = centerY + math.sin(angle) * radius * 0.58
            self.create_text(
                x,
                y,
                text=str(number),
                fill=self.style.numberColor,
                font=("Helvetica", fontSize, "bold"),
            )

    def _drawHands(self, centerX: float, centerY: float, radius: float) -> None:
        """Draw hour, minute, and second hands."""
        now = self.currentDateTime
        hour = now.hour % 12
        minute = now.minute
        second = now.second

        hourAngle = math.radians((hour + minute / 60) * 30 - 90)
        minuteAngle = math.radians((minute + second / 60) * 6 - 90)
        secondAngle = math.radians(second * 6 - 90)

        self._drawHand(centerX, centerY, radius * 0.38, hourAngle, self.style.hourHandColor, max(5, int(radius * 0.05)))
        self._drawHand(centerX, centerY, radius * 0.60, minuteAngle, self.style.minuteHandColor, max(3, int(radius * 0.033)))
        if self.showSeconds:
            self._drawHand(centerX, centerY, radius * 0.74, secondAngle, self.style.secondHandColor, max(1, int(radius * 0.010)))
            tailX = centerX + math.cos(secondAngle + math.pi) * radius * 0.14
            tailY = centerY + math.sin(secondAngle + math.pi) * radius * 0.14
            self.create_line(
                centerX,
                centerY,
                tailX,
                tailY,
                fill=self.style.secondHandColor,
                width=max(1, int(radius * 0.010)),
                capstyle=tk.ROUND,
            )

    def _drawHand(self, centerX: float, centerY: float, length: float, angle: float, color: str, width: int) -> None:
        """Draw a single hand from the center to the given angle."""
        endX = centerX + math.cos(angle) * length
        endY = centerY + math.sin(angle) * length
        self.create_line(
            centerX,
            centerY,
            endX,
            endY,
            fill=color,
            width=width,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND,
        )

    def _drawCenterCap(self, centerX: float, centerY: float, radius: float) -> None:
        """Draw the center cap over the hands."""
        self.create_oval(
            centerX - radius * 0.08,
            centerY - radius * 0.08,
            centerX + radius * 0.08,
            centerY + radius * 0.08,
            fill=self.theme.textColor,
            outline=self.style.ringColor,
            width=2,
        )
        self.create_oval(
            centerX - radius * 0.035,
            centerY - radius * 0.035,
            centerX + radius * 0.035,
            centerY + radius * 0.035,
            fill=self.style.secondHandColor,
            outline="",
        )

    def _drawDateInfo(self, centerX: float, centerY: float, radius: float) -> None:
        """Draw a small integrated date line inside the dial."""
        weekdayNames = ("Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom")
        monthNames = (
            "Ene",
            "Feb",
            "Mar",
            "Abr",
            "May",
            "Jun",
            "Jul",
            "Ago",
            "Sep",
            "Oct",
            "Nov",
            "Dic",
        )
        weekday = weekdayNames[self.currentDateTime.weekday()]
        day = f"{self.currentDateTime.day:02d}"
        month = monthNames[self.currentDateTime.month - 1]
        year = self.currentDateTime.year
        capsuleY = centerY + radius * 0.40
        self.create_rectangle(
            centerX - radius * 0.42,
            capsuleY - 18,
            centerX + radius * 0.42,
            capsuleY + 18,
            fill="#0f172a",
            outline=self.style.ringColor,
            width=1,
        )
        self.create_text(
            centerX,
            capsuleY,
            text=f"{weekday} · {day} {month} {year}",
            fill=self.theme.textColor,
            font=("Helvetica", max(9, int(radius * 0.055)), "bold"),
        )


def buildDefaultThemes() -> list[ThemePalette]:
    """Return the predefined dark-friendly application themes."""
    return [
        ThemePalette(
            name="Nocturno",
            appBackground="#080c14",
            panelBackground="#121826",
            surfaceBackground="#1c2538",
            textColor="#ffffff",
            mutedTextColor="#94a3b8",
            accentColor="#38bdf8",
            accentHoverColor="#0ea5e9",
            borderColor="#1e293b",
        ),
        ThemePalette(
            name="Grafito",
            appBackground="#0f172a",
            panelBackground="#1e293b",
            surfaceBackground="#334155",
            textColor="#f8fafc",
            mutedTextColor="#94a3b8",
            accentColor="#fbbf24",
            accentHoverColor="#f59e0b",
            borderColor="#475569",
        ),
        ThemePalette(
            name="Azul profundo",
            appBackground="#0a192f",
            panelBackground="#112240",
            surfaceBackground="#233554",
            textColor="#e6f1ff",
            mutedTextColor="#8892b0",
            accentColor="#64ffda",
            accentHoverColor="#52e0c4",
            borderColor="#1d2d50",
        ),
        ThemePalette(
            name="Esmeralda",
            appBackground="#064e3b",
            panelBackground="#065f46",
            surfaceBackground="#047857",
            textColor="#ecfdf5",
            mutedTextColor="#a7f3d0",
            accentColor="#34d399",
            accentHoverColor="#10b981",
            borderColor="#059669",
        ),
    ]


def buildDefaultClockStyles() -> list[ClockStylePreset]:
    """Return the predefined clock style presets."""
    return [
        ClockStylePreset(
            name="Clásico elegante",
            dialBackground="#f8fafc",
            ringColor="#d4af37",
            numberColor="#1e293b",
            hourHandColor="#334155",
            minuteHandColor="#475569",
            secondHandColor="#ef4444",
            showNumbers=True,
            showMinuteMarks=True,
            showDateInfo=True,
        ),
        ClockStylePreset(
            name="Deportivo",
            dialBackground="#0f172a",
            ringColor="#38bdf8",
            numberColor="#f8fafc",
            hourHandColor="#fbbf24",
            minuteHandColor="#e2e8f0",
            secondHandColor="#22c55e",
            showNumbers=True,
            showMinuteMarks=True,
            showDateInfo=False,
        ),
        ClockStylePreset(
            name="Minimalista",
            dialBackground="#ffffff",
            ringColor="#e2e8f0",
            numberColor="#0f172a",
            hourHandColor="#0f172a",
            minuteHandColor="#0f172a",
            secondHandColor="#94a3b8",
            showNumbers=True,
            showMinuteMarks=False,
            showDateInfo=False,
        ),
        ClockStylePreset(
            name="Vintage",
            dialBackground="#fdf6e3",
            ringColor="#b58900",
            numberColor="#073642",
            hourHandColor="#586e75",
            minuteHandColor="#657b83",
            secondHandColor="#dc322f",
            showNumbers=True,
            showMinuteMarks=True,
            showDateInfo=True,
        ),
        ClockStylePreset(
            name="Premium moderno",
            dialBackground="#1e293b",
            ringColor="#94a3b8",
            numberColor="#ffffff",
            hourHandColor="#ffffff",
            minuteHandColor="#cbd5e1",
            secondHandColor="#fb7185",
            showNumbers=True,
            showMinuteMarks=True,
            showDateInfo=True,
        ),
    ]
"""Service layer for reusable UI animations."""

from __future__ import annotations

from PySide6.QtCore import QPoint, QPropertyAnimation
from PySide6.QtWidgets import QWidget


class AnimationService:
    """Creates animation objects that can be reused in UI components."""

    def createFadeAnimation(self, target: QWidget, durationMs: int = 250) -> QPropertyAnimation:
        """Create a fade-like animation using window opacity."""
        animation = QPropertyAnimation(target, b"windowOpacity")
        animation.setDuration(durationMs)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        return animation

    def createSlideAnimation(self, target: QWidget, startPoint: QPoint, endPoint: QPoint, durationMs: int = 250) -> QPropertyAnimation:
        """Create a simple position slide animation."""
        animation = QPropertyAnimation(target, b"pos")
        animation.setDuration(durationMs)
        animation.setStartValue(startPoint)
        animation.setEndValue(endPoint)
        return animation

    def createPulseAnimation(self, target: QWidget, durationMs: int = 300) -> QPropertyAnimation:
        """Create a basic pulse animation placeholder on geometry."""
        animation = QPropertyAnimation(target, b"geometry")
        animation.setDuration(durationMs)
        return animation

"""
دکمه‌های نئونی، شیشه‌ای و خطر با آیکون SVG یکپارچه
"""
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from app.styles.icons import get_icon


class NeonButton(QPushButton):
    def __init__(self, text: str, svg_name: str = "", parent=None):
        super().__init__(text, parent)
        self.setObjectName("neonBtn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(42)

        if svg_name:
            self.setIcon(get_icon(svg_name, size=16, color="#ffffff"))
            self.setIconSize(QSize(16, 16))

        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(20)
        glow.setColor(QColor(191, 90, 242, 120))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)


class GhostButton(QPushButton):
    def __init__(self, text: str, svg_name: str = "", parent=None):
        super().__init__(text, parent)
        self.setObjectName("ghostBtn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(42)

        if svg_name:
            self.setIcon(get_icon(svg_name, size=16, color="#e8e8f0"))
            self.setIconSize(QSize(16, 16))


class DangerButton(QPushButton):
    def __init__(self, text: str, svg_name: str = "", parent=None):
        super().__init__(text, parent)
        self.setObjectName("dangerBtn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(42)

        if svg_name:
            self.setIcon(get_icon(svg_name, size=16, color="#ff453a"))
            self.setIconSize(QSize(16, 16))
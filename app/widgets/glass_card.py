"""
کارت شیشه‌ای پایه + StatCard با آیکون SVG یکپارچه
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor
from app.styles.icons import get_pixmap


class GlassCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("glassCard")
        self._apply_shadow()

    def _apply_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)


class StatCard(GlassCard):
    def __init__(self, svg_name: str, value: str, label: str,
                 accent_color: str = "#00d4ff", parent=None):
        super().__init__(parent)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setMinimumHeight(120)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # آیکون با رنگ هماهنگ
        icon_lbl = QLabel()
        icon_lbl.setPixmap(get_pixmap(svg_name, 26, accent_color))
        icon_lbl.setFixedSize(56, 56)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(191,90,242,0.3),
                stop:1 rgba(0,212,255,0.3));
            border: 1px solid {accent_color};
            border-radius: 16px;
        """)
        layout.addWidget(icon_lbl)

        text_box = QVBoxLayout()
        text_box.setSpacing(4)

        self.value_lbl = QLabel(value)
        self.value_lbl.setObjectName("cardValue")
        self.value_lbl.setStyleSheet(
            f"color: {accent_color}; font-size: 28px; font-weight: 700;"
        )

        self.label_lbl = QLabel(label)
        self.label_lbl.setObjectName("cardSubtext")

        text_box.addWidget(self.value_lbl)
        text_box.addWidget(self.label_lbl)
        text_box.addStretch()

        layout.addLayout(text_box)
        layout.addStretch()

    def set_value(self, value: str):
        self.value_lbl.setText(value)
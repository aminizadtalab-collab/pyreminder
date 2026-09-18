"""
سایدبار Apple-Style با آیکون‌های SVG
"""
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QButtonGroup, QFrame
)
from PyQt6.QtGui import QIcon
from app.config import SIDEBAR_WIDTH, icon_path


class SidebarItem(QPushButton):
    def __init__(self, svg_name: str, text: str, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebarItem")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIcon(QIcon(icon_path(svg_name)))
        self.setIconSize(QSize(20, 20))
        self.setText(f"  {text}")
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setMinimumHeight(46)


class Sidebar(QWidget):
    page_changed = pyqtSignal(int)

    ITEMS = [
        ("home", "داشبورد"),
        ("add", "افزودن یادآور"),
        ("list", "لیست یادآورها"),
        ("chart", "آمار و تحلیل"),
        ("settings", "تنظیمات"),
    ]

    def __init__(self, profile: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(SIDEBAR_WIDTH)
        self.profile = profile
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(6)

        # لوگو
        logo_row = QHBoxLayout()
        logo_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_icon = QLabel()
        logo_icon.setPixmap(
            QIcon(icon_path("app_icon")).pixmap(QSize(36, 36))
        )
        logo_row.addWidget(logo_icon)

        layout.addLayout(logo_row)

        app_name = QLabel("Glass Reminder")
        app_name.setStyleSheet(
            "color: white; font-size: 15px; font-weight: 600; padding-bottom: 20px;"
        )
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(app_name)

        # جداکننده
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: rgba(255,255,255,0.08); border: none; max-height: 1px;")
        layout.addWidget(sep)
        layout.addSpacing(10)

        # آیتم‌ها
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for index, (svg_name, text) in enumerate(self.ITEMS):
            btn = SidebarItem(svg_name, text)
            self.button_group.addButton(btn, index)
            layout.addWidget(btn)

        self.button_group.buttons()[0].setChecked(True)
        self.button_group.idClicked.connect(self.page_changed.emit)

        layout.addStretch()

        # پروفایل
        self._add_profile_card(layout)

    def _add_profile_card(self, parent_layout):
        card = QWidget()
        card.setObjectName("profileCard")
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(12, 10, 12, 10)
        card_layout.setSpacing(10)
        card.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        avatar = QLabel()
        avatar.setPixmap(
            QIcon(icon_path("user")).pixmap(QSize(24, 24))
        )
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #bf5af2, stop:1 #00d4ff);
            border-radius: 20px;
        """)
        card_layout.addWidget(avatar)

        info_box = QVBoxLayout()
        info_box.setSpacing(2)

        name = QLabel(self.profile.get("name", "کاربر"))
        name.setStyleSheet("color: white; font-size: 13px; font-weight: 600;")

        role = QLabel(self.profile.get("role", "توسعه‌دهنده"))
        role.setStyleSheet("color: #a0a0b8; font-size: 11px;")

        info_box.addWidget(name)
        info_box.addWidget(role)
        card_layout.addLayout(info_box)
        card_layout.addStretch()

        parent_layout.addWidget(card)
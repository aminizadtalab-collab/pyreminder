"""
پاپ‌آپ نمایش ریمایندر با آیکون SVG یکپارچه
"""
from datetime import datetime
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QApplication
)
from app.widgets.neon_button import NeonButton, GhostButton, DangerButton
from app.styles.icons import get_pixmap


class ReminderPopup(QDialog):
    def __init__(self, task: dict, parent=None):
        super().__init__(parent)
        self.task = task
        self.result_action: str | None = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Dialog
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(440, 340)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 460, 40)

        self._setup_ui()
        self._animate_in()

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setStyleSheet("""
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(20, 20, 35, 245),
                stop:1 rgba(15, 15, 30, 245)
            );
            border: 1px solid rgba(191, 90, 242, 0.5);
            border-radius: 22px;
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # هدر
        header_row = QHBoxLayout()
        header_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bell_icon = QLabel()
        bell_icon.setPixmap(get_pixmap("bell", 28, "#00d4ff"))
        bell_icon.setStyleSheet("border: none; background: transparent;")
        header_row.addWidget(bell_icon)

        header = QLabel("یادآوری")
        header.setStyleSheet("""
            color: #00d4ff; font-size: 20px; font-weight: 700;
            border: none; background: transparent; padding-right: 8px;
        """)
        header_row.addWidget(header)
        layout.addLayout(header_row)

        # عنوان تسک
        name = QLabel(self.task["name"])
        name.setStyleSheet("""
            color: white; font-size: 17px; font-weight: 600;
            border: none; background: transparent; padding: 8px;
        """)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name.setWordWrap(True)
        layout.addWidget(name)

        # توضیحات
        if self.task.get("description"):
            desc = QLabel(self.task["description"])
            desc.setStyleSheet("""
                color: #a0a0b8; font-size: 13px;
                border: none; background: transparent;
            """)
            desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc.setWordWrap(True)
            layout.addWidget(desc)

        # اطلاعات دسته‌بندی و اولویت
        info_row = QHBoxLayout()
        info_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_row.setSpacing(10)

        cat_icon = QLabel()
        cat_icon.setPixmap(get_pixmap("category", 14, "#bf5af2"))
        cat_icon.setStyleSheet("border: none; background: transparent;")
        info_row.addWidget(cat_icon)

        cat_text = QLabel(self.task["category"])
        cat_text.setStyleSheet(
            "color: #bf5af2; font-size: 12px; font-weight: 500;"
            " border: none; background: transparent;"
        )
        info_row.addWidget(cat_text)

        info_row.addSpacing(12)

        pri_icon = QLabel()
        pri_icon.setPixmap(get_pixmap("priority", 14, "#ff9f0a"))
        pri_icon.setStyleSheet("border: none; background: transparent;")
        info_row.addWidget(pri_icon)

        pri_text = QLabel(self.task["priority"])
        pri_text.setStyleSheet(
            "color: #ff9f0a; font-size: 12px; font-weight: 500;"
            " border: none; background: transparent;"
        )
        info_row.addWidget(pri_text)

        layout.addLayout(info_row)

        # ساعت
        time_row = QHBoxLayout()
        time_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        time_icon = QLabel()
        time_icon.setPixmap(get_pixmap("clock", 16, "#ff9f0a"))
        time_icon.setStyleSheet("border: none; background: transparent;")
        time_row.addWidget(time_icon)

        time_lbl = QLabel(datetime.now().strftime("%H:%M"))
        time_lbl.setStyleSheet("""
            color: #ff9f0a; font-size: 14px; font-weight: 600;
            border: none; background: transparent; padding-right: 6px;
        """)
        time_row.addWidget(time_lbl)
        layout.addLayout(time_row)

        layout.addStretch()

        # دکمه‌ها
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        done_btn = NeonButton("انجام شد", "check_circle")
        done_btn.clicked.connect(lambda: self._respond("done"))

        snooze_btn = GhostButton("۱۰ دقیقه بعد", "snooze")
        snooze_btn.clicked.connect(lambda: self._respond("snooze"))

        dismiss_btn = DangerButton("رد", "dismiss")
        dismiss_btn.clicked.connect(lambda: self._respond("dismiss"))

        btn_row.addWidget(done_btn)
        btn_row.addWidget(snooze_btn)
        btn_row.addWidget(dismiss_btn)
        layout.addLayout(btn_row)

        outer.addWidget(container)

    def _animate_in(self):
        self.setWindowOpacity(0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(400)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()

    def _respond(self, action: str):
        self.result_action = action
        self.accept()
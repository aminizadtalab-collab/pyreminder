"""
صفحه افزودن یادآور با آیکون SVG یکپارچه
"""
from datetime import datetime
from PyQt6.QtCore import Qt, QTime, QDate, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QTextEdit, QComboBox, QTimeEdit,
    QDateEdit, QSpinBox, QMessageBox
)
from app.widgets.glass_card import GlassCard
from app.widgets.neon_button import NeonButton, GhostButton
from app.config import CATEGORIES, PRIORITIES, REPEAT_OPTIONS
from app.styles.icons import get_pixmap


class AddTaskPage(QWidget):
    task_added = pyqtSignal()

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        title = QLabel("افزودن یادآور جدید")
        title.setObjectName("pageTitle")
        subtitle = QLabel("جزئیات یادآور را وارد کنید")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # فرم
        form_card = GlassCard()
        form = QGridLayout(form_card)
        form.setContentsMargins(28, 28, 28, 28)
        form.setSpacing(16)
        form.setVerticalSpacing(20)

        # عنوان
        form.addWidget(self._icon_label("title", "عنوان"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("مثلاً: تمرین پایتون، مدیتیشن صبحگاهی...")
        self.name_input.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        form.addWidget(self.name_input, 1, 0, 1, 2)

        # توضیحات
        form.addWidget(self._icon_label("note", "توضیحات"), 2, 0)
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("توضیحات اضافی...")
        self.desc_input.setMaximumHeight(90)
        self.desc_input.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        form.addWidget(self.desc_input, 3, 0, 1, 2)

        # دسته‌بندی و اولویت
        form.addWidget(self._icon_label("category", "دسته‌بندی"), 4, 0)
        form.addWidget(self._icon_label("priority", "اولویت"), 4, 1)

        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES)
        self.category_combo.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(PRIORITIES)
        self.priority_combo.setCurrentIndex(2)
        self.priority_combo.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        form.addWidget(self.category_combo, 5, 0)
        form.addWidget(self.priority_combo, 5, 1)

        # زمان و تاریخ
        form.addWidget(self._icon_label("clock", "ساعت"), 6, 0)
        form.addWidget(self._icon_label("calendar", "تاریخ"), 6, 1)

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime.currentTime())

        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("yyyy/MM/dd")
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)

        form.addWidget(self.time_edit, 7, 0)
        form.addWidget(self.date_edit, 7, 1)

        # تکرار و مدت
        form.addWidget(self._icon_label("repeat", "تکرار"), 8, 0)
        form.addWidget(self._icon_label("duration", "مدت (دقیقه)"), 8, 1)

        self.repeat_combo = QComboBox()
        self.repeat_combo.addItems(REPEAT_OPTIONS)
        self.repeat_combo.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(5, 480)
        self.duration_spin.setValue(30)
        self.duration_spin.setSuffix(" دقیقه")

        form.addWidget(self.repeat_combo, 9, 0)
        form.addWidget(self.duration_spin, 9, 1)

        layout.addWidget(form_card)

        # دکمه‌ها
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        btn_row.addStretch()

        clear_btn = GhostButton("پاک کردن", "clean")
        clear_btn.clicked.connect(self._clear_form)

        submit_btn = NeonButton("ثبت یادآور", "sparkle")
        submit_btn.clicked.connect(self._submit)

        btn_row.addWidget(clear_btn)
        btn_row.addWidget(submit_btn)
        layout.addLayout(btn_row)

        layout.addStretch()

    def _icon_label(self, svg_name: str, text: str) -> QWidget:
        widget = QWidget()
        h = QHBoxLayout(widget)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(6)

        icon = QLabel()
        icon.setPixmap(get_pixmap(svg_name, 14, "#a0a0b8"))
        h.addWidget(icon)

        lbl = QLabel(text)
        lbl.setObjectName("sectionLabel")
        h.addWidget(lbl)
        h.addStretch()
        return widget

    def _clear_form(self):
        self.name_input.clear()
        self.desc_input.clear()
        self.time_edit.setTime(QTime.currentTime())
        self.date_edit.setDate(QDate.currentDate())
        self.category_combo.setCurrentIndex(0)
        self.priority_combo.setCurrentIndex(2)
        self.repeat_combo.setCurrentIndex(0)
        self.duration_spin.setValue(30)

    def _submit(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "خطا", "لطفاً عنوان یادآور را وارد کنید!")
            return

        task = {
            "id": datetime.now().timestamp(),
            "name": name,
            "description": self.desc_input.toPlainText().strip(),
            "category": self.category_combo.currentText(),
            "priority": self.priority_combo.currentText(),
            "time": self.time_edit.time().toString("HH:mm"),
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "repeat": self.repeat_combo.currentText(),
            "duration": self.duration_spin.value(),
            "done": False,
            "created": datetime.now().isoformat(),
            "snooze_until": None,
            "notified_today": False,
        }

        self.dm.add_task(task)
        self._clear_form()
        self.task_added.emit()

        QMessageBox.information(self, "موفق", f"«{name}» با موفقیت اضافه شد!")
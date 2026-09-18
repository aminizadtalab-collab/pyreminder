"""
صفحه لیست یادآورها با آیکون SVG یکپارچه
"""
from datetime import datetime
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QListWidget, QListWidgetItem,
    QProgressBar, QMessageBox
)
from app.widgets.glass_card import GlassCard
from app.widgets.neon_button import NeonButton, GhostButton, DangerButton
from app.config import CATEGORIES, PRIORITY_COLORS
from app.styles.icons import get_pixmap, get_priority_icon


class TaskListPage(QWidget):
    tasks_changed = pyqtSignal()

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        title = QLabel("لیست یادآورها")
        title.setObjectName("pageTitle")
        subtitle = QLabel("مدیریت و پیگیری همه یادآورها")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # فیلترها
        filter_card = GlassCard()
        f_layout = QHBoxLayout(filter_card)
        f_layout.setContentsMargins(16, 12, 16, 12)
        f_layout.setSpacing(10)

        search_icon = QLabel()
        search_icon.setPixmap(get_pixmap("search", 16, "#a0a0b8"))
        f_layout.addWidget(search_icon)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجو در یادآورها...")
        self.search_input.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.search_input.textChanged.connect(self.refresh)
        f_layout.addWidget(self.search_input, stretch=2)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(
            ["همه", "در انتظار", "انجام شده"] + CATEGORIES
        )
        self.filter_combo.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.filter_combo.currentTextChanged.connect(self.refresh)
        f_layout.addWidget(self.filter_combo, stretch=1)

        layout.addWidget(filter_card)

        # پیشرفت
        progress_card = GlassCard()
        p_layout = QHBoxLayout(progress_card)
        p_layout.setContentsMargins(16, 12, 16, 12)

        prog_icon = QLabel()
        prog_icon.setPixmap(get_pixmap("chart", 16, "#00d4ff"))
        p_layout.addWidget(prog_icon)

        p_label = QLabel("  پیشرفت امروز")
        p_label.setObjectName("cardTitle")
        p_layout.addWidget(p_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFormat("%p%")
        p_layout.addWidget(self.progress_bar, stretch=1)

        self.progress_count = QLabel("0/0")
        self.progress_count.setStyleSheet("color: #00d4ff; font-weight: 600;")
        p_layout.addWidget(self.progress_count)

        layout.addWidget(progress_card)

        # لیست
        self.list_widget = QListWidget()
        self.list_widget.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        layout.addWidget(self.list_widget, stretch=1)

        # دکمه‌ها
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        done_btn = NeonButton("تغییر وضعیت", "check_circle")
        done_btn.clicked.connect(self._toggle_done)

        delete_btn = DangerButton("حذف", "delete")
        delete_btn.clicked.connect(self._delete)

        refresh_btn = GhostButton("بروزرسانی", "refresh")
        refresh_btn.clicked.connect(self.refresh)

        btn_row.addWidget(done_btn)
        btn_row.addWidget(delete_btn)
        btn_row.addWidget(refresh_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    def refresh(self):
        self.list_widget.clear()
        filter_text = self.filter_combo.currentText()
        search = self.search_input.text().strip().lower()

        today = datetime.now().strftime("%Y-%m-%d")
        total_today, done_today = 0, 0

        for task in self.dm.tasks:
            if filter_text == "انجام شده" and not task.get("done"):
                continue
            if filter_text == "در انتظار" and task.get("done"):
                continue
            if filter_text in CATEGORIES and task["category"] != filter_text:
                continue
            if search and search not in task["name"].lower() \
                    and search not in task.get("description", "").lower():
                continue

            if task["date"] == today or task.get("repeat") != "بدون تکرار":
                total_today += 1
                if task.get("done"):
                    done_today += 1

            status = "[انجام شد]" if task.get("done") else "[در انتظار]"
            item_text = (
                f"{status}  {task['name']}\n"
                f"    {task['time']}   |   {task['date']}   |   "
                f"{task['category']}   |   {task['repeat']}"
            )
            if task.get("description"):
                item_text += f"\n    {task['description'][:60]}"

            item = QListWidgetItem(item_text)
            item.setIcon(get_priority_icon(task["priority"]))
            item.setData(Qt.ItemDataRole.UserRole, task["id"])

            if task.get("done"):
                item.setForeground(QColor("#30d158"))
            else:
                color = PRIORITY_COLORS.get(task["priority"], "#ffffff")
                item.setForeground(QColor(color))

            self.list_widget.addItem(item)

        if total_today > 0:
            self.progress_bar.setValue(int(done_today / total_today * 100))
            self.progress_count.setText(f"{done_today}/{total_today}")
        else:
            self.progress_bar.setValue(0)
            self.progress_count.setText("0/0")

    def _selected_task(self):
        current = self.list_widget.currentItem()
        if not current:
            QMessageBox.warning(self, "خطا", "یک مورد را انتخاب کنید!")
            return None
        return self.dm.get_task(current.data(Qt.ItemDataRole.UserRole))

    def _toggle_done(self):
        task = self._selected_task()
        if task:
            self.dm.update_task(task["id"], {"done": not task.get("done")})
            self.refresh()
            self.tasks_changed.emit()

    def _delete(self):
        task = self._selected_task()
        if not task:
            return
        reply = QMessageBox.question(
            self, "تایید حذف",
            f"«{task['name']}» حذف شود؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.dm.remove_task(task["id"])
            self.refresh()
            self.tasks_changed.emit()
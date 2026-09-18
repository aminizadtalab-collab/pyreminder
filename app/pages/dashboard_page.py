"""
صفحه داشبورد اصلی با آیکون SVG یکپارچه
"""
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QListWidget, QListWidgetItem
)
from app.widgets.glass_card import GlassCard, StatCard
from app.styles.icons import get_pixmap, get_priority_icon


class DashboardPage(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # هدر
        header_box = QVBoxLayout()
        header_box.setSpacing(4)

        title = QLabel("خوش آمدید")
        title.setObjectName("pageTitle")
        subtitle = QLabel("خلاصه‌ای از یادآورها و پیشرفت شما")
        subtitle.setObjectName("pageSubtitle")

        header_box.addWidget(title)
        header_box.addWidget(subtitle)
        layout.addLayout(header_box)

        # کارت‌های آمار
        stats_grid = QGridLayout()
        stats_grid.setSpacing(16)

        self.card_total = StatCard("list", "0", "کل یادآورها", "#00d4ff")
        self.card_done = StatCard("check_circle", "0", "انجام شده", "#30d158")
        self.card_pending = StatCard("pending", "0", "در انتظار", "#ff9f0a")
        self.card_today = StatCard("calendar", "0", "برای امروز", "#bf5af2")

        stats_grid.addWidget(self.card_total, 0, 0)
        stats_grid.addWidget(self.card_done, 0, 1)
        stats_grid.addWidget(self.card_pending, 0, 2)
        stats_grid.addWidget(self.card_today, 0, 3)

        layout.addLayout(stats_grid)

        # لیست یادآورهای پیش رو
        upcoming_card = GlassCard()
        up_layout = QVBoxLayout(upcoming_card)
        up_layout.setContentsMargins(20, 20, 20, 20)

        up_header = QHBoxLayout()
        up_icon = QLabel()
        up_icon.setPixmap(get_pixmap("clock", 18, "#00d4ff"))
        up_header.addWidget(up_icon)

        up_title = QLabel("  یادآورهای پیش رو")
        up_title.setObjectName("cardTitle")
        up_header.addWidget(up_title)
        up_header.addStretch()
        up_layout.addLayout(up_header)

        self.upcoming_list = QListWidget()
        self.upcoming_list.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        up_layout.addWidget(self.upcoming_list)

        layout.addWidget(upcoming_card, stretch=1)

    def refresh(self):
        tasks = self.dm.tasks
        total = len(tasks)
        done = sum(1 for t in tasks if t.get("done"))
        pending = total - done

        today = datetime.now().strftime("%Y-%m-%d")
        today_tasks = [
            t for t in tasks if t["date"] == today and not t.get("done")
        ]

        self.card_total.set_value(str(total))
        self.card_done.set_value(str(done))
        self.card_pending.set_value(str(pending))
        self.card_today.set_value(str(len(today_tasks)))

        self.upcoming_list.clear()
        upcoming = sorted(
            [t for t in tasks if not t.get("done")],
            key=lambda x: (x["date"], x["time"])
        )[:8]

        if not upcoming:
            item = QListWidgetItem("هیچ یادآور فعالی ندارید")
            self.upcoming_list.addItem(item)
            return

        for t in upcoming:
            text = (
                f"  {t['name']}\n"
                f"    {t['time']}   |   {t['date']}   |   {t['category']}"
            )
            item = QListWidgetItem(text)
            item.setIcon(get_priority_icon(t["priority"]))
            self.upcoming_list.addItem(item)
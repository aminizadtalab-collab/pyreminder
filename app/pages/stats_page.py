"""
صفحه آمار و تحلیل با آیکون SVG یکپارچه
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QProgressBar
)
from app.widgets.glass_card import GlassCard, StatCard
from app.widgets.neon_button import GhostButton
from app.styles.icons import get_pixmap


class CategoryRow(QWidget):
    def __init__(self, category: str, done: int, total: int, parent=None):
        super().__init__(parent)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 6, 0, 6)
        layout.setSpacing(12)

        name = QLabel(category)
        name.setStyleSheet("color: white; font-size: 13px; font-weight: 500;")
        name.setFixedWidth(180)
        layout.addWidget(name)

        pct = int((done / total) * 100) if total > 0 else 0
        bar = QProgressBar()
        bar.setValue(pct)
        bar.setFormat(f"{done}/{total}  |  %p%")
        bar.setFixedHeight(18)
        layout.addWidget(bar, stretch=1)


class StatsPage(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        title = QLabel("آمار و تحلیل")
        title.setObjectName("pageTitle")
        subtitle = QLabel("نگاهی جامع به عملکرد شما")
        subtitle.setObjectName("pageSubtitle")
        self.main_layout.addWidget(title)
        self.main_layout.addWidget(subtitle)

        # کارت‌های آمار
        stats_grid = QGridLayout()
        stats_grid.setSpacing(16)

        self.card_total = StatCard("chart", "0", "کل یادآورها", "#00d4ff")
        self.card_done = StatCard("check_circle", "0", "تکمیل شده", "#30d158")
        self.card_rate = StatCard("target", "0%", "نرخ موفقیت", "#bf5af2")
        self.card_xp = StatCard("fire", "0", "امتیاز XP", "#ff9f0a")

        stats_grid.addWidget(self.card_total, 0, 0)
        stats_grid.addWidget(self.card_done, 0, 1)
        stats_grid.addWidget(self.card_rate, 0, 2)
        stats_grid.addWidget(self.card_xp, 0, 3)

        self.main_layout.addLayout(stats_grid)

        # کارت دسته‌بندی
        self.cat_card = GlassCard()
        self.cat_layout = QVBoxLayout(self.cat_card)
        self.cat_layout.setContentsMargins(24, 20, 24, 20)
        self.cat_layout.setSpacing(6)

        cat_header = QHBoxLayout()
        cat_icon = QLabel()
        cat_icon.setPixmap(get_pixmap("folder", 18, "#00d4ff"))
        cat_header.addWidget(cat_icon)

        cat_title = QLabel("  آمار دسته‌بندی‌ها")
        cat_title.setObjectName("cardTitle")
        cat_header.addWidget(cat_title)
        cat_header.addStretch()

        self.cat_layout.addLayout(cat_header)
        self.cat_layout.addSpacing(10)

        self.main_layout.addWidget(self.cat_card, stretch=1)

        # دکمه بروزرسانی
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        refresh_btn = GhostButton("بروزرسانی آمار", "refresh")
        refresh_btn.clicked.connect(self.refresh)
        btn_row.addWidget(refresh_btn)
        self.main_layout.addLayout(btn_row)

    def refresh(self):
        tasks = self.dm.tasks
        total = len(tasks)
        done = sum(1 for t in tasks if t.get("done"))
        rate = int((done / total) * 100) if total > 0 else 0
        xp = done * 10

        self.card_total.set_value(str(total))
        self.card_done.set_value(str(done))
        self.card_rate.set_value(f"{rate}%")
        self.card_xp.set_value(str(xp))

        # پاک کردن ردیف‌های قبلی
        while self.cat_layout.count() > 2:
            item = self.cat_layout.takeAt(2)
            if item.widget():
                item.widget().deleteLater()

        categories = {}
        for t in tasks:
            cat = t["category"]
            if cat not in categories:
                categories[cat] = {"total": 0, "done": 0}
            categories[cat]["total"] += 1
            if t.get("done"):
                categories[cat]["done"] += 1

        if not categories:
            empty = QLabel("هنوز یادآوری اضافه نشده است")
            empty.setStyleSheet("color: #6c6c80; padding: 20px;")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cat_layout.addWidget(empty)
            return

        for cat, info in sorted(categories.items(), key=lambda x: -x[1]["total"]):
            row = CategoryRow(cat, info["done"], info["total"])
            self.cat_layout.addWidget(row)

        self.cat_layout.addStretch()
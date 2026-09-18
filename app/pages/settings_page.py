"""
صفحه تنظیمات (کاملاً سازگار با ویندوز و لینوکس)
"""
import os
import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox, QSpinBox, QMessageBox
)
from app.widgets.glass_card import GlassCard
from app.widgets.neon_button import GhostButton, DangerButton
from app.styles.icons import get_pixmap


class SettingsPage(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        title = QLabel("تنظیمات")
        title.setObjectName("pageTitle")
        subtitle = QLabel("رفتار برنامه را شخصی‌سازی کنید")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # صدا
        sound_card = self._create_card("sound", "صدا و نوتیفیکیشن")
        self.sound_check = QCheckBox("فعال‌سازی صدای یادآوری")
        self.sound_check.setChecked(self.dm.settings.get("sound", True))
        self.sound_check.stateChanged.connect(self._save)
        sound_card.layout().addWidget(self.sound_check)
        layout.addWidget(sound_card)

        # تکرار
        repeat_card = self._create_card("repeat", "تکرار خودکار یادآوری")
        self.repeat_check = QCheckBox("اگر یادآور انجام نشد، دوباره یادآوری کن")
        self.repeat_check.setChecked(self.dm.settings.get("repeat", True))
        self.repeat_check.stateChanged.connect(self._save)
        repeat_card.layout().addWidget(self.repeat_check)

        interval_row = QHBoxLayout()
        interval_lbl = QLabel("فاصله تکرار:")
        interval_lbl.setStyleSheet("color: #a0a0b8;")
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(5, 60)
        self.interval_spin.setValue(self.dm.settings.get("repeat_interval", 10))
        self.interval_spin.setSuffix(" دقیقه")
        self.interval_spin.valueChanged.connect(self._save)
        interval_row.addWidget(interval_lbl)
        interval_row.addWidget(self.interval_spin)
        interval_row.addStretch()
        repeat_card.layout().addLayout(interval_row)
        layout.addWidget(repeat_card)

        # اجرا با سیستم
        startup_card = self._create_card("startup", "اجرای خودکار")
        self.startup_check = QCheckBox("شروع برنامه همراه با سیستم")
        self.startup_check.setChecked(self.dm.settings.get("startup", False))
        self.startup_check.stateChanged.connect(self._toggle_startup)
        startup_card.layout().addWidget(self.startup_check)
        layout.addWidget(startup_card)

        # مدیریت داده
        data_card = self._create_card("data", "مدیریت داده‌ها")
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        clear_done_btn = GhostButton("حذف یادآورهای انجام‌شده", "delete")
        clear_done_btn.clicked.connect(self._clear_done)

        clear_all_btn = DangerButton("حذف تمام داده‌ها", "warning")
        clear_all_btn.clicked.connect(self._clear_all)

        btn_row.addWidget(clear_done_btn)
        btn_row.addWidget(clear_all_btn)
        btn_row.addStretch()
        data_card.layout().addLayout(btn_row)
        layout.addWidget(data_card)

        # درباره
        about_card = self._create_card("info", "درباره برنامه")
        about_lbl = QLabel(
            "Glass Reminder v2.0\n"
            "یادآور شیشه‌ای مدرن با طراحی Glassmorphism\n"
            "طراحی‌شده برای لینوکس و ویندوز"
        )
        about_lbl.setStyleSheet("color: #a0a0b8; padding: 8px 0;")
        about_card.layout().addWidget(about_lbl)
        layout.addWidget(about_card)

        layout.addStretch()

    def _create_card(self, svg_name: str, title_text: str) -> GlassCard:
        card = GlassCard()
        v = QVBoxLayout(card)
        v.setContentsMargins(22, 18, 22, 18)
        v.setSpacing(12)

        header = QHBoxLayout()
        icon = QLabel()
        icon.setPixmap(get_pixmap(svg_name, 18, "#00d4ff"))
        header.addWidget(icon)

        title = QLabel(f"  {title_text}")
        title.setObjectName("cardTitle")
        header.addWidget(title)
        header.addStretch()
        v.addLayout(header)

        return card

    def _save(self):
        self.dm.update_setting("sound", self.sound_check.isChecked())
        self.dm.update_setting("repeat", self.repeat_check.isChecked())
        self.dm.update_setting("repeat_interval", self.interval_spin.value())

    def _toggle_startup(self):
        enabled = self.startup_check.isChecked()
        self.dm.update_setting("startup", enabled)

        if sys.platform == "win32":
            # ویندوز: قرار دادن اسکریپت لودر در پوشه Startup ویندوز
            startup_dir = os.path.join(
                os.environ.get("APPDATA", ""),
                r"Microsoft\Windows\Start Menu\Programs\Startup"
            )
            bat_file = os.path.join(startup_dir, "glass-reminder.bat")
            if enabled:
                main_script = os.path.abspath(sys.argv[0])
                # اجرای مخفی بدون باز شدن ترمینال مشکی (با pythonw یا مستقیم از exe)
                if main_script.endswith(".exe"):
                    with open(bat_file, "w", encoding="utf-8") as f:
                        f.write(f'@start "" "{main_script}"\n')
                else:
                    with open(bat_file, "w", encoding="utf-8") as f:
                        f.write(f'@start "" pythonw "{main_script}"\n')
            else:
                if os.path.exists(bat_file):
                    os.remove(bat_file)
        else:
            # لینوکس
            autostart_dir = os.path.expanduser("~/.config/autostart")
            desktop_file = os.path.join(autostart_dir, "glass-reminder.desktop")

            if enabled:
                os.makedirs(autostart_dir, exist_ok=True)
                main_script = os.path.abspath(sys.argv[0])
                with open(desktop_file, "w") as f:
                    f.write(
                        "[Desktop Entry]\n"
                        "Type=Application\n"
                        "Name=Glass Reminder\n"
                        f"Exec=python3 {main_script}\n"
                        "Hidden=false\n"
                        "X-GNOME-Autostart-enabled=true\n"
                    )
            else:
                if os.path.exists(desktop_file):
                    os.remove(desktop_file)

    def _clear_done(self):
        reply = QMessageBox.question(
            self, "تایید",
            "همه یادآورهای انجام‌شده حذف شوند؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.dm.data["tasks"] = [t for t in self.dm.tasks if not t.get("done")]
            self.dm.save()
            QMessageBox.information(self, "انجام شد", "پاک‌سازی انجام شد")

    def _clear_all(self):
        reply = QMessageBox.question(
            self, "هشدار",
            "⚠️ همه یادآورها برای همیشه حذف می‌شوند. مطمئن هستید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.dm.data["tasks"] = []
            self.dm.save()
            QMessageBox.information(self, "انجام شد", "همه داده‌ها حذف شدند")
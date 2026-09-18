"""
نقطه ورود برنامه Glass Reminder
"""
import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication

from app.main_window import MainWindow
from app.config import FONTS_DIR


def load_custom_fonts():
    """بارگذاری فونت‌های سفارشی از پوشه assets/fonts"""
    if not os.path.exists(FONTS_DIR):
        return
    for f in os.listdir(FONTS_DIR):
        if f.lower().endswith((".ttf", ".otf")):
            QFontDatabase.addApplicationFont(os.path.join(FONTS_DIR, f))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Glass Reminder")
    app.setQuitOnLastWindowClosed(False)  # مخفی در tray

    # جهت راست به چپ (فارسی)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    # فونت
    load_custom_fonts()
    font = QFont("Inter, Vazirmatn, SF Pro Display, Segoe UI, Tahoma", 10)
    app.setFont(font)

    # پنجره اصلی
    window = MainWindow()
    window.show()

    # وسط‌چین
    screen = app.primaryScreen().geometry()
    x = (screen.width() - window.width()) // 2
    y = (screen.height() - window.height()) // 2
    window.move(x, y)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
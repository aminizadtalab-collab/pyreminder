"""
نوار عنوان سفارشی با آیکون‌های SVG یکپارچه
"""
from datetime import datetime
from PyQt6.QtCore import Qt, QTimer, QPoint, QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from app.config import TITLE_BAR_HEIGHT, APP_NAME
from app.styles.icons import get_icon, get_pixmap


class WindowButton(QPushButton):
    def __init__(self, icon_name: str, tooltip: str,
                 is_close: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("winBtnClose" if is_close else "winBtn")
        self.setFixedSize(32, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        color = "#ff453a" if is_close else "#a0a0b8"
        self.setIcon(get_icon(icon_name, size=14, color=color))
        self.setIconSize(QSize(14, 14))
        self.setToolTip(tooltip)


class TitleBar(QWidget):
    minimize_clicked = pyqtSignal()
    maximize_clicked = pyqtSignal()
    hide_clicked = pyqtSignal()
    close_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setFixedHeight(TITLE_BAR_HEIGHT)
        self._drag_pos: QPoint | None = None
        self._setup_ui()
        self._setup_clock()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 12, 0)
        layout.setSpacing(10)

        # آیکون اپ
        app_icon = QLabel()
        app_icon.setPixmap(get_pixmap("diamond", 18))
        app_icon.setFixedSize(22, 22)
        layout.addWidget(app_icon)

        # عنوان
        self.title_label = QLabel(APP_NAME)
        self.title_label.setObjectName("appTitle")
        layout.addWidget(self.title_label)

        layout.addStretch()

        # آیکون ساعت + ساعت
        clock_icon = QLabel()
        clock_icon.setPixmap(get_pixmap("clock", 14, "#00d4ff"))
        layout.addWidget(clock_icon)

        self.clock_label = QLabel()
        self.clock_label.setObjectName("clockLabel")
        layout.addWidget(self.clock_label)

        layout.addSpacing(20)

        # دکمه‌های کنترل پنجره (سمت راست)
        self.btn_hide = WindowButton("hide", "مخفی در System Tray")
        self.btn_hide.clicked.connect(self.hide_clicked.emit)

        self.btn_min = WindowButton("minimize", "Minimize")
        self.btn_min.clicked.connect(self.minimize_clicked.emit)

        self.btn_max = WindowButton("maximize", "Maximize / Restore")
        self.btn_max.clicked.connect(self.maximize_clicked.emit)

        self.btn_close = WindowButton("close", "Close", is_close=True)
        self.btn_close.clicked.connect(self.close_clicked.emit)

        for b in (self.btn_hide, self.btn_min, self.btn_max, self.btn_close):
            layout.addWidget(b)

    def _setup_clock(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_clock)
        self.timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        now = datetime.now()
        self.clock_label.setText(now.strftime("%H:%M:%S    %Y/%m/%d"))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = (
                event.globalPosition().toPoint()
                - self.window().frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self._drag_pos:
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def mouseDoubleClickEvent(self, event):
        self.maximize_clicked.emit()
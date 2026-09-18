"""
پنجره اصلی برنامه با آیکون SVG یکپارچه
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QAction
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QSystemTrayIcon, QMenu, QApplication,
    QGraphicsDropShadowEffect, QDialog
)

from app.config import WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT, APP_NAME
from app.styles.stylesheet import get_main_stylesheet
from app.styles.icons import get_icon
from app.core.data_manager import DataManager
from app.core.reminder_engine import ReminderEngine
from app.core.notification import NotificationService

from app.widgets.title_bar import TitleBar
from app.widgets.sidebar import Sidebar
from app.widgets.reminder_popup import ReminderPopup

from app.pages.dashboard_page import DashboardPage
from app.pages.add_task_page import AddTaskPage
from app.pages.task_list_page import TaskListPage
from app.pages.stats_page import StatsPage
from app.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowIcon(get_icon("app_icon", 64))

        self.dm = DataManager()
        self.engine = ReminderEngine(self.dm, self)
        self.engine.reminder_triggered.connect(self._show_reminder_popup)

        self._is_maximized = False
        self._normal_geometry = None

        self._setup_ui()
        self._setup_tray()
        self.setStyleSheet(get_main_stylesheet())
        self.engine.start()

    def _setup_ui(self):
        root = QWidget()
        root.setObjectName("rootWidget")
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(12, 12, 12, 12)

        bg = QWidget()
        bg.setObjectName("backgroundWidget")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(191, 90, 242, 100))
        shadow.setOffset(0, 0)
        bg.setGraphicsEffect(shadow)

        outer.addWidget(bg)

        bg_layout = QVBoxLayout(bg)
        bg_layout.setContentsMargins(0, 0, 0, 0)
        bg_layout.setSpacing(0)

        self.title_bar = TitleBar()
        self.title_bar.minimize_clicked.connect(self.showMinimized)
        self.title_bar.maximize_clicked.connect(self._toggle_maximize)
        self.title_bar.hide_clicked.connect(self._hide_to_tray)
        self.title_bar.close_clicked.connect(self.close)
        bg_layout.addWidget(self.title_bar)

        body = QWidget()
        body.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.sidebar = Sidebar(self.dm.data.get("profile", {}))
        self.sidebar.page_changed.connect(self._change_page)
        body_layout.addWidget(self.sidebar)

        content_wrapper = QWidget()
        content_wrapper.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(32, 24, 32, 24)

        self.stack = QStackedWidget()

        self.dashboard_page = DashboardPage(self.dm)
        self.add_page = AddTaskPage(self.dm)
        self.list_page = TaskListPage(self.dm)
        self.stats_page = StatsPage(self.dm)
        self.settings_page = SettingsPage(self.dm)

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.add_page)
        self.stack.addWidget(self.list_page)
        self.stack.addWidget(self.stats_page)
        self.stack.addWidget(self.settings_page)

        self.add_page.task_added.connect(self._on_data_changed)
        self.list_page.tasks_changed.connect(self._on_data_changed)

        content_layout.addWidget(self.stack)
        body_layout.addWidget(content_wrapper, stretch=1)

        bg_layout.addWidget(body, stretch=1)

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(get_icon("app_icon", 64))
        self.tray.setToolTip(APP_NAME)

        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background: #12121a;
                color: white;
                border: 1px solid rgba(191,90,242,0.4);
                border-radius: 10px;
                padding: 6px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 6px;
            }
            QMenu::item:selected {
                background: rgba(191,90,242,0.3);
            }
        """)

        show_act = QAction(get_icon("list", 16), "نمایش برنامه", self)
        show_act.triggered.connect(self._show_from_tray)
        menu.addAction(show_act)

        add_act = QAction(get_icon("add", 16), "افزودن سریع", self)
        add_act.triggered.connect(
            lambda: (self._show_from_tray(), self._change_page(1))
        )
        menu.addAction(add_act)

        menu.addSeparator()

        quit_act = QAction(get_icon("close", 16, "#ff453a"), "خروج", self)
        quit_act.triggered.connect(QApplication.quit)
        menu.addAction(quit_act)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    def _on_tray_activated(self, reason):
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self._show_from_tray()

    def _show_from_tray(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def _hide_to_tray(self):
        self.hide()
        self.tray.showMessage(
            APP_NAME,
            "برنامه در پس‌زمینه فعال است",
            QSystemTrayIcon.MessageIcon.Information,
            2500,
        )

    def _change_page(self, index: int):
        self.stack.setCurrentIndex(index)
        for btn in self.sidebar.button_group.buttons():
            btn.setChecked(self.sidebar.button_group.id(btn) == index)
        if index == 0:
            self.dashboard_page.refresh()
        elif index == 2:
            self.list_page.refresh()
        elif index == 3:
            self.stats_page.refresh()

    def _on_data_changed(self):
        self.dashboard_page.refresh()
        self.list_page.refresh()
        self.stats_page.refresh()

    def _show_reminder_popup(self, task: dict):
        if self.dm.settings.get("sound", True):
            NotificationService.play_sound()

        NotificationService.send_system_notification(
            "یادآوری",
            f"{task['name']}\n{task.get('description', '')}",
            urgency="critical",
        )

        popup = ReminderPopup(task, self)
        if popup.exec() == QDialog.DialogCode.Accepted:
            if popup.result_action == "done":
                self.dm.update_task(task["id"], {"done": True})
                self._on_data_changed()
            elif popup.result_action == "snooze":
                self.engine.snooze_task(task["id"], minutes=10)

    def _toggle_maximize(self):
        if self._is_maximized:
            if self._normal_geometry:
                self.setGeometry(self._normal_geometry)
            self._is_maximized = False
        else:
            self._normal_geometry = self.geometry()
            screen = QApplication.primaryScreen().availableGeometry()
            self.setGeometry(screen)
            self._is_maximized = True

    def closeEvent(self, event):
        event.ignore()
        self._hide_to_tray()
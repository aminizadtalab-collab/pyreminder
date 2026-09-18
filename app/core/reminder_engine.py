"""
موتور بررسی و اجرای ریمایندرها
"""
from datetime import datetime, timedelta
from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class ReminderEngine(QObject):
    reminder_triggered = pyqtSignal(dict)

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager

        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_reminders)

        self.reset_timer = QTimer(self)
        self.reset_timer.timeout.connect(self._daily_reset)

    def start(self, interval_ms: int = 30_000):
        self.check_timer.start(interval_ms)
        self.reset_timer.start(60_000)

    def stop(self):
        self.check_timer.stop()
        self.reset_timer.stop()

    def _daily_reset(self):
        now = datetime.now()
        if now.hour == 0 and now.minute == 0:
            for task in self.dm.tasks:
                task["notified_today"] = False
            self.dm.save()

    def check_reminders(self):
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_day = now.weekday()

        for task in self.dm.tasks:
            if task.get("done"):
                continue

            # snooze check
            snooze_until = task.get("snooze_until")
            if snooze_until:
                if now >= datetime.fromisoformat(snooze_until):
                    task["snooze_until"] = None
                    task["notified_today"] = False
                else:
                    continue
            elif task.get("notified_today"):
                continue

            if self._should_trigger(task, now, current_date, current_day):
                self.reminder_triggered.emit(task)
                task["notified_today"] = True
                self.dm.save()

    def _should_trigger(self, task, now, current_date, current_day) -> bool:
        try:
            task_dt = datetime.strptime(
                f"{task['date']} {task['time']}", "%Y-%m-%d %H:%M"
            )
        except ValueError:
            return False

        diff_sec = abs((now - task_dt).total_seconds())
        time_match = diff_sec < 90

        repeat = task.get("repeat", "بدون تکرار")

        if repeat == "بدون تکرار":
            return task["date"] == current_date and time_match
        if repeat == "هر روز":
            return time_match
        if repeat == "هر هفته":
            try:
                orig = datetime.strptime(task["date"], "%Y-%m-%d").weekday()
                return current_day == orig and time_match
            except ValueError:
                return False
        if repeat == "هر ماه":
            try:
                orig = datetime.strptime(task["date"], "%Y-%m-%d").day
                return now.day == orig and time_match
            except ValueError:
                return False
        if repeat.startswith("روزهای کاری"):
            return current_day in [5, 6, 0, 1, 2] and time_match
        if repeat == "هر ۲ ساعت":
            t_time = datetime.strptime(task["time"], "%H:%M")
            return (now.minute == t_time.minute
                    and now.hour % 2 == t_time.hour % 2)
        if repeat == "هر ۳۰ دقیقه":
            t_time = datetime.strptime(task["time"], "%H:%M")
            return now.minute % 30 == t_time.minute % 30

        return False

    def snooze_task(self, task_id: float, minutes: int = 10):
        task = self.dm.get_task(task_id)
        if task:
            snooze = datetime.now() + timedelta(minutes=minutes)
            task["snooze_until"] = snooze.isoformat()
            task["notified_today"] = False
            self.dm.save()
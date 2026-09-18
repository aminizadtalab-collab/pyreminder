"""
سیستم نوتیفیکیشن و صدا (کاملاً سازگار با ویندوز و لینوکس)
"""
import sys
import subprocess


class NotificationService:
    @staticmethod
    def play_sound():
        if sys.platform == "win32":
            try:
                import winsound
                # پخش صدای اعلان استاندارد ویندوز
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except Exception:
                pass
        else:
            # لینوکس
            sound_paths = [
                "/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga",
                "/usr/share/sounds/freedesktop/stereo/complete.oga",
                "/usr/share/sounds/alsa/Front_Center.wav",
            ]
            for path in sound_paths:
                try:
                    subprocess.Popen(
                        ["paplay", path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    return
                except FileNotFoundError:
                    continue
            try:
                subprocess.Popen(
                    ["aplay", "/usr/share/sounds/alsa/Front_Center.wav"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except Exception:
                pass

    @staticmethod
    def send_system_notification(title: str, body: str, urgency: str = "normal"):
        if sys.platform == "win32":
            # در ویندوز نوتیفیکیشن‌ها از طریق سیستم‌تری هندل می‌شوند
            pass
        else:
            # لینوکس
            try:
                subprocess.Popen([
                    "notify-send",
                    title, body,
                    f"--urgency={urgency}",
                    "--expire-time=8000",
                    "--app-name=Glass Reminder",
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                pass
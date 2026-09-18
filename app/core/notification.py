"""
سیستم نوتیفیکیشن (صدا + notify-send)
"""
import subprocess
from typing import Optional


class NotificationService:
    SOUND_PATHS = [
        "/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga",
        "/usr/share/sounds/freedesktop/stereo/complete.oga",
        "/usr/share/sounds/alsa/Front_Center.wav",
    ]

    @staticmethod
    def play_sound():
        for path in NotificationService.SOUND_PATHS:
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
            subprocess.Popen(["aplay", NotificationService.SOUND_PATHS[-1]],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    @staticmethod
    def send_system_notification(title: str, body: str, urgency: str = "normal"):
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
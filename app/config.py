"""
پیکربندی سراسری برنامه
"""
import os

APP_NAME = "Glass Reminder"
APP_VERSION = "2.0.0"

# مسیرها
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

DATA_DIR = os.path.expanduser("~/.config/glass-reminder")
DATA_FILE = os.path.join(DATA_DIR, "data.json")
os.makedirs(DATA_DIR, exist_ok=True)

# ابعاد پنجره
WINDOW_MIN_WIDTH = 1100
WINDOW_MIN_HEIGHT = 720
SIDEBAR_WIDTH = 260
TITLE_BAR_HEIGHT = 48

# تایمرها
REMINDER_CHECK_INTERVAL = 30_000
CLOCK_UPDATE_INTERVAL = 1_000

# دسته‌بندی‌ها
CATEGORIES = [
    "کار",
    "مهارت / یادگیری",
    "ورزش",
    "سلامتی",
    "هنر",
    "دارو",
    "خرید",
    "تماس",
    "سایر",
]

PRIORITIES = ["فوری", "مهم", "معمولی", "کم‌اهمیت"]

PRIORITY_COLORS = {
    "فوری": "#ff453a",
    "مهم": "#ff9f0a",
    "معمولی": "#00d4ff",
    "کم‌اهمیت": "#30d158",
}

REPEAT_OPTIONS = [
    "بدون تکرار",
    "هر روز",
    "هر هفته",
    "هر ماه",
    "روزهای کاری (شنبه-چهارشنبه)",
    "هر ۲ ساعت",
    "هر ۳۰ دقیقه",
]
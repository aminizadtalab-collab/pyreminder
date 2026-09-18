"""
═══════════════════════════════════════════════════════════
  Glass Reminder — Unified SVG Icon System
  تمام آیکون‌های SVG در یک ماژول با پشتیبانی رنگ داینامیک
═══════════════════════════════════════════════════════════

استفاده:
    from app.styles.icons import get_icon, get_pixmap

    btn.setIcon(get_icon("home"))
    btn.setIcon(get_icon("delete", color="#ff453a"))
    label.setPixmap(get_pixmap("bell", size=28, color="#00d4ff"))
"""

from __future__ import annotations
import os
from PyQt6.QtCore import QByteArray, QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer


# ═══════════════════════════════════════════════════════════
#   قالب پایه برای آیکون‌های Stroke-Based (خطی)
# ═══════════════════════════════════════════════════════════

_STROKE_TEMPLATE = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    'stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
    'stroke-linejoin="round">{body}</svg>'
)


# ═══════════════════════════════════════════════════════════
#   بدنه آیکون‌های خطی  (name: (body, stroke_width))
# ═══════════════════════════════════════════════════════════

_STROKE_ICONS: dict[str, tuple[str, float]] = {

    # ─────────── ناوبری / Navigation ───────────
    "home": (
        '<path d="M3 9.5L12 3l9 6.5V20a1.5 1.5 0 01-1.5 1.5h-4V15a1 1 0 '
        '00-1-1h-3a1 1 0 00-1 1v6.5H6A1.5 1.5 0 014.5 20z"/>',
        1.8,
    ),

    "add": (
        '<circle cx="12" cy="12" r="9.5"/>'
        '<line x1="12" y1="8" x2="12" y2="16"/>'
        '<line x1="8" y1="12" x2="16" y2="12"/>',
        1.8,
    ),

    "list": (
        '<rect x="3" y="3" width="18" height="18" rx="3"/>'
        '<line x1="8" y1="8" x2="17" y2="8"/>'
        '<line x1="8" y1="12" x2="17" y2="12"/>'
        '<line x1="8" y1="16" x2="13" y2="16"/>'
        '<line x1="5.5" y1="8" x2="5.51" y2="8"/>'
        '<line x1="5.5" y1="12" x2="5.51" y2="12"/>'
        '<line x1="5.5" y1="16" x2="5.51" y2="16"/>',
        1.8,
    ),

    "chart": (
        '<rect x="3" y="14" width="4" height="7" rx="1"/>'
        '<rect x="10" y="8" width="4" height="13" rx="1"/>'
        '<rect x="17" y="3" width="4" height="18" rx="1"/>',
        1.8,
    ),

    "settings": (
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 01-2.83 '
        '2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 '
        '0 01-4 0v-.09a1.65 1.65 0 00-1.08-1.51 1.65 1.65 0 00-1.82.33l-.06.06a2 '
        '2 0 01-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 '
        '00-1.51-1H3a2 2 0 010-4h.09a1.65 1.65 0 001.51-1.08 1.65 1.65 0 '
        '00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06a1.65 1.65 0 '
        '001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 '
        '001.08 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 '
        '2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9c.26.6.85 1.02 1.51 '
        '1.08H21a2 2 0 010 4h-.09c-.66.06-1.25.48-1.51 1.08z"/>',
        1.8,
    ),

    # ─────────── کنترل پنجره / Window Controls ───────────
    "close": (
        '<line x1="18" y1="6" x2="6" y2="18"/>'
        '<line x1="6" y1="6" x2="18" y2="18"/>',
        2.0,
    ),

    "minimize": (
        '<line x1="6" y1="12" x2="18" y2="12"/>',
        2.0,
    ),

    "maximize": (
        '<rect x="4" y="4" width="16" height="16" rx="2"/>',
        1.8,
    ),

    "restore": (
        '<rect x="7" y="7" width="13" height="13" rx="2"/>'
        '<path d="M4 16V6a2 2 0 012-2h10"/>',
        1.8,
    ),

    "hide": (
        '<polyline points="6 9 12 15 18 9"/>',
        1.8,
    ),

    "chevron_down": (
        '<polyline points="6 9 12 15 18 9"/>',
        2.0,
    ),

    "chevron_up": (
        '<polyline points="18 15 12 9 6 15"/>',
        2.0,
    ),

    # ─────────── زمان / Time ───────────
    "clock": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polyline points="12 6 12 12 16 14"/>',
        1.8,
    ),

    "calendar": (
        '<rect x="3" y="4" width="18" height="18" rx="2"/>'
        '<line x1="16" y1="2" x2="16" y2="6"/>'
        '<line x1="8" y1="2" x2="8" y2="6"/>'
        '<line x1="3" y1="10" x2="21" y2="10"/>'
        '<line x1="8" y1="14.5" x2="8.01" y2="14.5"/>'
        '<line x1="12" y1="14.5" x2="12.01" y2="14.5"/>'
        '<line x1="16" y1="14.5" x2="16.01" y2="14.5"/>'
        '<line x1="8" y1="18" x2="8.01" y2="18"/>'
        '<line x1="12" y1="18" x2="12.01" y2="18"/>',
        1.8,
    ),

    "duration": (
        '<circle cx="12" cy="13" r="8"/>'
        '<path d="M5 3L2 6"/>'
        '<path d="M22 6l-3-3"/>'
        '<path d="M12 9v4l2.5 2.5"/>',
        1.8,
    ),

    "snooze": (
        '<circle cx="12" cy="13" r="8"/>'
        '<path d="M12 9v4l2.5 2.5"/>'
        '<path d="M5 3L2 6"/>'
        '<path d="M22 6l-3-3"/>'
        '<path d="M6.5 19.5L4.5 21.5"/>'
        '<path d="M17.5 19.5l2 2"/>',
        1.8,
    ),

    "pending": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="M12 6v6l4 2"/>',
        1.8,
    ),

    "repeat": (
        '<polyline points="17 1 21 5 17 9"/>'
        '<path d="M3 11V9a4 4 0 014-4h14"/>'
        '<polyline points="7 23 3 19 7 15"/>'
        '<path d="M21 13v2a4 4 0 01-4 4H3"/>',
        1.8,
    ),

    # ─────────── عملیات / Actions ───────────
    "check": (
        '<polyline points="20 6 9 17 4 12"/>',
        2.2,
    ),

    "check_circle": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polyline points="16 9 10.5 15 8 12.5"/>',
        1.8,
    ),

    "dismiss": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="15" y1="9" x2="9" y2="15"/>'
        '<line x1="9" y1="9" x2="15" y2="15"/>',
        1.8,
    ),

    "delete": (
        '<polyline points="3 6 5 6 21 6"/>'
        '<path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/>'
        '<path d="M10 11v6"/>'
        '<path d="M14 11v6"/>'
        '<path d="M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2"/>',
        1.8,
    ),

    "edit": (
        '<path d="M17 3a2.83 2.83 0 114 4L7.5 20.5 2 22l1.5-5.5z"/>'
        '<line x1="15" y1="5" x2="19" y2="9"/>',
        1.8,
    ),

    "refresh": (
        '<polyline points="23 4 23 10 17 10"/>'
        '<polyline points="1 20 1 14 7 14"/>'
        '<path d="M3.51 9a9 9 0 0114.85-3.36L23 10"/>'
        '<path d="M20.49 15a9 9 0 01-14.85 3.36L1 14"/>',
        1.8,
    ),

    "search": (
        '<circle cx="11" cy="11" r="8"/>'
        '<line x1="21" y1="21" x2="16.65" y2="16.65"/>',
        1.8,
    ),

    "filter": (
        '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
        1.8,
    ),

    "clean": (
        '<path d="M3 6h18"/>'
        '<path d="M8 6V4a1 1 0 011-1h6a1 1 0 011 1v2"/>'
        '<path d="M6 6l1 13a2 2 0 002 2h6a2 2 0 002-2l1-13"/>'
        '<path d="M10 11l4 4"/>'
        '<path d="M14 11l-4 4"/>',
        1.8,
    ),

    "save": (
        '<path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/>'
        '<polyline points="17 21 17 13 7 13 7 21"/>'
        '<polyline points="7 3 7 8 15 8"/>',
        1.8,
    ),

    # ─────────── فرم / Form Fields ───────────
    "title": (
        '<path d="M4 7V4h16v3"/>'
        '<path d="M9 20h6"/>'
        '<path d="M12 4v16"/>',
        1.8,
    ),

    "note": (
        '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="16" y1="13" x2="8" y2="13"/>'
        '<line x1="16" y1="17" x2="8" y2="17"/>',
        1.8,
    ),

    "category": (
        '<path d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 '
        '8.59a2 2 0 010 2.82z"/>'
        '<line x1="7" y1="7" x2="7.01" y2="7"/>',
        1.8,
    ),

    "priority": (
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
        1.8,
    ),

    "folder": (
        '<path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 '
        '2 0 012 2z"/>',
        1.8,
    ),

    # ─────────── سیستم / System ───────────
    "bell": (
        '<path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/>'
        '<path d="M13.73 21a2 2 0 01-3.46 0"/>',
        1.8,
    ),

    "sound": (
        '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>'
        '<path d="M19.07 4.93a10 10 0 010 14.14"/>'
        '<path d="M15.54 8.46a5 5 0 010 7.07"/>',
        1.8,
    ),

    "startup": (
        '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 '
        '2.18 0 00-2.91-.09z"/>'
        '<path d="M12 15l-3-3a22 22 0 012-3.95A12.88 12.88 0 0122 2c0 2.72-.78 '
        '7.5-6 11a22.35 22.35 0 01-4 2z"/>'
        '<path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/>'
        '<path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
        1.8,
    ),

    "data": (
        '<ellipse cx="12" cy="5" rx="9" ry="3"/>'
        '<path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>'
        '<path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
        1.8,
    ),

    "info": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="12" y1="16" x2="12" y2="12"/>'
        '<line x1="12" y1="8" x2="12.01" y2="8"/>',
        1.8,
    ),

    "warning": (
        '<path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 '
        '001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>'
        '<line x1="12" y1="9" x2="12" y2="13"/>'
        '<line x1="12" y1="17" x2="12.01" y2="17"/>',
        1.8,
    ),

    "user": (
        '<path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>'
        '<circle cx="12" cy="7" r="4"/>',
        1.8,
    ),

    # ─────────── آمار / Stats ───────────
    "target": (
        '<circle cx="12" cy="12" r="10"/>'
        '<circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>',
        1.8,
    ),

    "fire": (
        '<path d="M12 23c-4.97 0-9-2.69-9-6 0-4 5-11.44 8-12.5C11.33 5.5 12 7 '
        '12 7s2-4 4-4c0 3 1 5 2.5 7.5S21 15 21 17c0 3.31-4.03 6-9 6z"/>'
        '<path d="M12 23c-2.21 0-4-1.34-4-3 0-2 2.5-5.5 4-6 1.5.5 4 4 4 6 0 '
        '1.66-1.79 3-4 3z"/>',
        1.8,
    ),

    "sparkle": (
        '<path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/>',
        1.8,
    ),

    "trending": (
        '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>'
        '<polyline points="17 6 23 6 23 12"/>',
        1.8,
    ),
}


# ═══════════════════════════════════════════════════════════
#   آیکون‌های ویژه (با گرادیانت / رنگ ثابت)
# ═══════════════════════════════════════════════════════════

_SPECIAL_ICONS: dict[str, str] = {

    # لوگوی اصلی برنامه — گرادیانت بنفش→آبی نئون
    "app_icon": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">'
        '<defs>'
        '<linearGradient id="gA" x1="0" y1="0" x2="64" y2="64" '
        'gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#bf5af2"/>'
        '<stop offset="1" stop-color="#00d4ff"/>'
        '</linearGradient>'
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="2" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter>'
        '</defs>'
        '<rect x="4" y="4" width="56" height="56" rx="15" fill="url(#gA)"/>'
        '<rect x="4" y="4" width="56" height="56" rx="15" '
        'fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="1"/>'
        '<g filter="url(#glow)">'
        '<path d="M44 38c0-8-2-11-4-13.5V22a8 8 0 10-16 0v2.5C22 27 20 30 20 38l-3 '
        '4h30z" fill="none" stroke="#ffffff" stroke-width="2.6" '
        'stroke-linejoin="round" stroke-linecap="round"/>'
        '<path d="M28.5 46a3.5 3.5 0 007 0" fill="none" stroke="#ffffff" '
        'stroke-width="2.6" stroke-linecap="round"/>'
        '</g>'
        '</svg>'
    ),

    # الماس نئونی (لوگوی کوچک نوار عنوان)
    "diamond": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">'
        '<defs>'
        '<linearGradient id="gD" x1="0" y1="0" x2="24" y2="24" '
        'gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#bf5af2"/>'
        '<stop offset="1" stop-color="#00d4ff"/>'
        '</linearGradient>'
        '</defs>'
        '<path d="M6 3h12l4 6-10 13L2 9z" fill="url(#gD)" opacity="0.25"/>'
        '<path d="M6 3h12l4 6-10 13L2 9z" stroke="url(#gD)" stroke-width="1.8" '
        'stroke-linejoin="round" fill="none"/>'
        '<path d="M2 9h20" stroke="url(#gD)" stroke-width="1.4"/>'
        '<path d="M10 3l-2 6 4 13" stroke="url(#gD)" stroke-width="1.4" '
        'fill="none"/>'
        '<path d="M14 3l2 6-4 13" stroke="url(#gD)" stroke-width="1.4" '
        'fill="none"/>'
        '</svg>'
    ),

    # نشان اولویت — دایره‌های رنگی (برای لیست)
    "dot_urgent": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        '<circle cx="12" cy="12" r="6" fill="#ff453a"/>'
        '<circle cx="12" cy="12" r="9" fill="none" stroke="#ff453a" '
        'stroke-width="1.5" opacity="0.35"/></svg>'
    ),
    "dot_high": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        '<circle cx="12" cy="12" r="6" fill="#ff9f0a"/>'
        '<circle cx="12" cy="12" r="9" fill="none" stroke="#ff9f0a" '
        'stroke-width="1.5" opacity="0.35"/></svg>'
    ),
    "dot_normal": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        '<circle cx="12" cy="12" r="6" fill="#00d4ff"/>'
        '<circle cx="12" cy="12" r="9" fill="none" stroke="#00d4ff" '
        'stroke-width="1.5" opacity="0.35"/></svg>'
    ),
    "dot_low": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        '<circle cx="12" cy="12" r="6" fill="#30d158"/>'
        '<circle cx="12" cy="12" r="9" fill="none" stroke="#30d158" '
        'stroke-width="1.5" opacity="0.35"/></svg>'
    ),
}


# ═══════════════════════════════════════════════════════════
#   موتور رندر
# ═══════════════════════════════════════════════════════════

DEFAULT_COLOR = "#e8e8f0"
_pixmap_cache: dict[tuple, QPixmap] = {}

# آیکون جایگزین در صورت نبود نام
_FALLBACK = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    'stroke="{color}" stroke-width="1.8"><circle cx="12" cy="12" r="9"/>'
    '<line x1="12" y1="8" x2="12" y2="13"/>'
    '<line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
)


def svg_source(name: str, color: str = DEFAULT_COLOR) -> str:
    """کد خام SVG یک آیکون را برمی‌گرداند."""
    if name in _SPECIAL_ICONS:
        return _SPECIAL_ICONS[name]
    if name in _STROKE_ICONS:
        body, width = _STROKE_ICONS[name]
        return _STROKE_TEMPLATE.format(color=color, width=width, body=body)
    return _FALLBACK.format(color=color)


def get_pixmap(name: str, size: int = 24, color: str = DEFAULT_COLOR,
               dpr: float = 2.0) -> QPixmap:
    """
    رندر آیکون به QPixmap با پشتیبانی HiDPI.

    :param name:  نام آیکون
    :param size:  اندازه منطقی (پیکسل)
    :param color: رنگ (فقط برای آیکون‌های خطی)
    :param dpr:   ضریب چگالی پیکسل (کیفیت)
    """
    key = (name, size, color, dpr)
    if key in _pixmap_cache:
        return _pixmap_cache[key]

    source = svg_source(name, color)
    renderer = QSvgRenderer(QByteArray(source.encode("utf-8")))

    px = int(size * dpr)
    pixmap = QPixmap(px, px)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    renderer.render(painter)
    painter.end()

    pixmap.setDevicePixelRatio(dpr)
    _pixmap_cache[key] = pixmap
    return pixmap


def get_icon(name: str, size: int = 24, color: str = DEFAULT_COLOR) -> QIcon:
    """
    ساخت QIcon از آیکون SVG.
    حالت‌های Normal / Disabled به‌صورت خودکار تولید می‌شوند.
    """
    icon = QIcon()
    icon.addPixmap(get_pixmap(name, size, color), QIcon.Mode.Normal)
    icon.addPixmap(get_pixmap(name, size, "#5a5a6e"), QIcon.Mode.Disabled)
    return icon


def get_priority_icon(priority: str) -> QIcon:
    """آیکون نقطه رنگی متناسب با اولویت."""
    mapping = {
        "فوری": "dot_urgent",
        "مهم": "dot_high",
        "معمولی": "dot_normal",
        "کم‌اهمیت": "dot_low",
    }
    return get_icon(mapping.get(priority, "dot_normal"), size=14)


def available_icons() -> list[str]:
    """لیست نام تمام آیکون‌های موجود."""
    return sorted(set(_STROKE_ICONS) | set(_SPECIAL_ICONS))


def clear_cache() -> None:
    """پاک کردن کش (مثلاً هنگام تغییر تم)."""
    _pixmap_cache.clear()


# ═══════════════════════════════════════════════════════════
#   ابزار جانبی: خروجی گرفتن به فایل‌های SVG (اختیاری)
# ═══════════════════════════════════════════════════════════

def export_all(directory: str, color: str = DEFAULT_COLOR) -> int:
    """
    تمام آیکون‌ها را به‌صورت فایل .svg در مسیر داده‌شده ذخیره می‌کند.
    (برای مواقعی که به فایل فیزیکی نیاز دارید)
    """
    os.makedirs(directory, exist_ok=True)
    count = 0
    for name in available_icons():
        path = os.path.join(directory, f"{name}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg_source(name, color))
        count += 1
    return count


if __name__ == "__main__":
    # اجرای مستقیم → خروجی فایل‌ها
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "./exported_icons"
    n = export_all(target)
    print(f"✔ {n} icon(s) exported to: {target}")
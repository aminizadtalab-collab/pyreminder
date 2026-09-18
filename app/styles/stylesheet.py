"""
QSS اصلی برنامه با استایل Glassmorphism + Neon
"""
from app.styles.theme import Theme as T


def get_main_stylesheet() -> str:
    return f"""
    /* ============ Main Window ============ */
    QMainWindow, QWidget#rootWidget {{
        background: transparent;
    }}

    QWidget#backgroundWidget {{
        background: qradialgradient(
            cx:0.15, cy:0.1, radius:0.9,
            fx:0.15, fy:0.1,
            stop:0 rgba(155, 92, 255, 55),
            stop:0.5 rgba(0, 212, 255, 25),
            stop:1 rgba(10, 10, 15, 255)
        );
        border-radius: {T.RADIUS_XL}px;
        border: 1px solid {T.BORDER_MEDIUM};
    }}

    /* ============ Title Bar ============ */
    QWidget#titleBar {{
        background: rgba(255, 255, 255, 0.03);
        border-top-left-radius: {T.RADIUS_XL}px;
        border-top-right-radius: {T.RADIUS_XL}px;
        border-bottom: 1px solid {T.BORDER_LIGHT};
    }}

    QLabel#appTitle {{
        color: {T.TEXT_PRIMARY};
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    QLabel#clockLabel {{
        color: {T.NEON_BLUE};
        font-size: 13px;
        font-weight: 500;
    }}

    QPushButton#winBtn {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid {T.BORDER_LIGHT};
        border-radius: 8px;
        color: {T.TEXT_SECONDARY};
        font-size: 14px;
        font-weight: bold;
    }}
    QPushButton#winBtn:hover {{
        background: rgba(255, 255, 255, 0.12);
        color: {T.TEXT_PRIMARY};
        border: 1px solid {T.BORDER_NEON};
    }}
    QPushButton#winBtnClose:hover {{
        background: rgba(255, 69, 58, 0.7);
        color: white;
        border: 1px solid {T.DANGER};
    }}

    /* ============ Sidebar ============ */
    QWidget#sidebar {{
        background: rgba(255, 255, 255, 0.04);
        border-left: 1px solid {T.BORDER_LIGHT};
    }}

    QLabel#sidebarLogo {{
        color: {T.NEON_PURPLE};
        font-size: 28px;
        font-weight: bold;
        padding: 20px 0;
    }}

    QPushButton#sidebarItem {{
        background: transparent;
        border: none;
        border-radius: {T.RADIUS_MD}px;
        color: {T.TEXT_SECONDARY};
        text-align: right;
        padding: 12px 16px;
        font-size: 14px;
        font-weight: 500;
    }}
    QPushButton#sidebarItem:hover {{
        background: rgba(255, 255, 255, 0.06);
        color: {T.TEXT_PRIMARY};
    }}
    QPushButton#sidebarItem:checked {{
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(191, 90, 242, 0.25),
            stop:1 rgba(0, 212, 255, 0.15)
        );
        color: {T.TEXT_PRIMARY};
        border: 1px solid {T.BORDER_NEON};
    }}

    QWidget#profileCard {{
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid {T.BORDER_LIGHT};
        border-radius: {T.RADIUS_MD}px;
    }}

    /* ============ Content Area ============ */
    QWidget#contentArea {{
        background: transparent;
    }}

    QLabel#pageTitle {{
        color: {T.TEXT_PRIMARY};
        font-size: 28px;
        font-weight: 700;
    }}
    QLabel#pageSubtitle {{
        color: {T.TEXT_SECONDARY};
        font-size: 14px;
        font-weight: 400;
    }}

    /* ============ Glass Cards ============ */
    QFrame#glassCard {{
        background: {T.BG_CARD};
        border: 1px solid {T.BORDER_LIGHT};
        border-radius: {T.RADIUS_LG}px;
    }}

    QLabel#cardTitle {{
        color: {T.TEXT_PRIMARY};
        font-size: 15px;
        font-weight: 600;
    }}
    QLabel#cardValue {{
        color: {T.NEON_BLUE};
        font-size: 32px;
        font-weight: 700;
    }}
    QLabel#cardSubtext {{
        color: {T.TEXT_SECONDARY};
        font-size: 12px;
    }}

    /* ============ Inputs ============ */
    QLineEdit, QTextEdit, QTimeEdit, QDateEdit, QSpinBox, QComboBox {{
        background: rgba(255, 255, 255, 0.04);
        color: {T.TEXT_PRIMARY};
        border: 1px solid {T.BORDER_LIGHT};
        border-radius: {T.RADIUS_SM}px;
        padding: 10px 14px;
        font-size: 13px;
        selection-background-color: {T.NEON_PURPLE};
    }}
    QLineEdit:focus, QTextEdit:focus, QTimeEdit:focus,
    QDateEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {T.NEON_PURPLE};
        background: rgba(255, 255, 255, 0.07);
    }}

    QComboBox::drop-down {{ border: none; width: 24px; }}
    QComboBox QAbstractItemView {{
        background: {T.BG_DARK};
        color: {T.TEXT_PRIMARY};
        border: 1px solid {T.BORDER_MEDIUM};
        border-radius: {T.RADIUS_SM}px;
        selection-background-color: {T.NEON_PURPLE};
        padding: 4px;
    }}

    /* ============ Buttons ============ */
    QPushButton#neonBtn {{
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {T.NEON_VIOLET},
            stop:1 {T.NEON_BLUE}
        );
        color: white;
        border: none;
        border-radius: {T.RADIUS_SM}px;
        padding: 12px 24px;
        font-size: 13px;
        font-weight: 600;
    }}
    QPushButton#neonBtn:hover {{
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {T.NEON_PURPLE},
            stop:1 {T.NEON_BLUE}
        );
    }}
    QPushButton#neonBtn:pressed {{
        background: {T.NEON_PURPLE};
    }}

    QPushButton#ghostBtn {{
        background: rgba(255, 255, 255, 0.05);
        color: {T.TEXT_PRIMARY};
        border: 1px solid {T.BORDER_MEDIUM};
        border-radius: {T.RADIUS_SM}px;
        padding: 10px 20px;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton#ghostBtn:hover {{
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid {T.NEON_BLUE};
    }}

    QPushButton#dangerBtn {{
        background: rgba(255, 69, 58, 0.15);
        color: {T.DANGER};
        border: 1px solid rgba(255, 69, 58, 0.4);
        border-radius: {T.RADIUS_SM}px;
        padding: 10px 20px;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton#dangerBtn:hover {{
        background: rgba(255, 69, 58, 0.3);
    }}

    /* ============ List Widget ============ */
    QListWidget {{
        background: transparent;
        border: none;
        outline: none;
    }}
    QListWidget::item {{
        background: {T.BG_CARD};
        border: 1px solid {T.BORDER_LIGHT};
        border-radius: {T.RADIUS_MD}px;
        padding: 14px;
        margin-bottom: 8px;
        color: {T.TEXT_PRIMARY};
    }}
    QListWidget::item:hover {{
        background: {T.BG_CARD_HOVER};
        border: 1px solid {T.BORDER_NEON};
    }}
    QListWidget::item:selected {{
        background: {T.BG_CARD_ACTIVE};
        border: 1px solid {T.NEON_PURPLE};
    }}

    /* ============ CheckBox ============ */
    QCheckBox {{ color: {T.TEXT_PRIMARY}; spacing: 10px; font-size: 13px; }}
    QCheckBox::indicator {{
        width: 20px; height: 20px;
        border-radius: 6px;
        border: 1px solid {T.BORDER_MEDIUM};
        background: rgba(255, 255, 255, 0.05);
    }}
    QCheckBox::indicator:checked {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {T.NEON_PURPLE}, stop:1 {T.NEON_BLUE});
        border: 1px solid {T.NEON_PURPLE};
    }}

    /* ============ ProgressBar ============ */
    QProgressBar {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid {T.BORDER_LIGHT};
        border-radius: 8px;
        height: 14px;
        text-align: center;
        color: {T.TEXT_PRIMARY};
        font-size: 11px;
    }}
    QProgressBar::chunk {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {T.NEON_PURPLE}, stop:1 {T.NEON_BLUE});
        border-radius: 7px;
    }}

    /* ============ ScrollBar ============ */
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: rgba(255, 255, 255, 0.15);
        border-radius: 4px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {T.NEON_PURPLE}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

    /* ============ Labels ============ */
    QLabel {{ color: {T.TEXT_PRIMARY}; font-size: 13px; }}
    QLabel#sectionLabel {{
        color: {T.TEXT_SECONDARY};
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    """
#!/bin/bash

# ============================================
#   Glass Reminder v2.0 - Installer (Fixed)
#   طراحی Glassmorphism برای لینوکس
# ============================================

set -e

# رنگ‌ها
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${PURPLE}"
echo "╔═══════════════════════════════════════════╗"
echo "║   ◆  Glass Reminder v2.0 Installer  ◆    ║"
echo "║   Glassmorphism Reminder for Linux       ║"
echo "╚═══════════════════════════════════════════╝"
echo -e "${NC}"

# ============== شناسایی توزیع ==============
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo -e "${RED}❌ توزیع سیستم شناسایی نشد!${NC}"
    exit 1
fi

echo -e "${CYAN}🔍 توزیع شناسایی‌شده: ${YELLOW}$DISTRO${NC}"

# ============== نصب پیش‌نیازها ==============
echo -e "\n${BLUE}📦 در حال نصب پیش‌نیازها...${NC}"

install_deps_debian() {
    sudo apt update
    # اضافه شدن python3-pyqt6.qtsvg برای حل خطای رندر آیکون‌های SVG
    sudo apt install -y \
        python3 python3-pip python3-pyqt6 python3-pyqt6.qtsvg \
        libnotify-bin pulseaudio-utils \
        fonts-inter || sudo apt install -y fonts-noto
}

install_deps_fedora() {
    sudo dnf install -y \
        python3 python3-pip python3-pyqt6 \
        libnotify pulseaudio-utils \
        google-noto-sans-fonts
}

install_deps_arch() {
    sudo pacman -Sy --noconfirm \
        python python-pip python-pyqt6 \
        libnotify libpulse \
        inter-font || sudo pacman -S --noconfirm noto-fonts
}

case $DISTRO in
    ubuntu|debian|linuxmint|pop)
        install_deps_debian
        ;;
    fedora|rhel|centos)
        install_deps_fedora
        ;;
    arch|manjaro|endeavouros)
        install_deps_arch
        ;;
    *)
        echo -e "${YELLOW}⚠️ توزیع ناشناخته. تلاش با pip...${NC}"
        pip3 install --user PyQt6
        ;;
esac

# fallback با pip در صورتی که PyQt6 سیستمی به هر دلیلی کار نکند
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo -e "${YELLOW}📥 نصب PyQt6 با pip...${NC}"
    pip3 install --user --break-system-packages PyQt6 2>/dev/null \
        || pip3 install --user PyQt6
fi

# ============== کپی فایل‌ها ==============
APP_DIR="$HOME/.local/share/glass-reminder"
echo -e "\n${BLUE}📁 در حال کپی فایل‌ها به ${APP_DIR}...${NC}"

mkdir -p "$APP_DIR"
cp -r main.py app "$APP_DIR/"

if [ -d "assets" ]; then
    cp -r assets "$APP_DIR/"
fi

chmod +x "$APP_DIR/main.py"

# ============== ساخت فایل دسکتاپ (.desktop) ==============
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/glass-reminder.desktop"
mkdir -p "$DESKTOP_DIR"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=Glass Reminder
Name[fa]=یادآور شیشه‌ای
Comment=Modern Glassmorphism Reminder App
Comment[fa]=یادآور مدرن با طراحی شیشه‌ای
Exec=python3 $APP_DIR/main.py
Icon=alarm
Terminal=false
Categories=Utility;Office;GTK;
StartupNotify=true
Keywords=reminder;task;todo;alarm;یادآور;
EOF

chmod +x "$DESKTOP_FILE"

# ============== ساخت اسکریپت اجرا در PATH ==============
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

cat > "$BIN_DIR/glass-reminder" << EOF
#!/bin/bash
cd "$APP_DIR"
python3 main.py "\$@"
EOF

chmod +x "$BIN_DIR/glass-reminder"

# ============== بروزرسانی دیتابیس دسکتاپ ==============
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

# ============== پایان ==============
echo -e "\n${GREEN}"
echo "╔═══════════════════════════════════════════╗"
echo "║  ✅  نصب با موفقیت انجام شد!             ║"
echo "╚═══════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "${CYAN}📌 روش‌های اجرا:${NC}"
echo -e "   ${YELLOW}۱.${NC} از منوی برنامه‌ها: جستجوی «Glass Reminder»"
echo -e "   ${YELLOW}۲.${NC} از ترمینال: ${GREEN}glass-reminder${NC}"
echo -e "   ${YELLOW}۳.${NC} مسیر مستقیم: ${GREEN}python3 $APP_DIR/main.py${NC}"
echo ""
echo -e "${PURPLE}◆  Glass Reminder برای شما آماده است  ◆${NC}\n"
#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🗑️  حذف Glass Reminder...${NC}"

rm -rf "$HOME/.local/share/glass-reminder"
rm -f "$HOME/.local/share/applications/glass-reminder.desktop"
rm -f "$HOME/.local/bin/glass-reminder"
rm -f "$HOME/.config/autostart/glass-reminder.desktop"

read -p "آیا داده‌های ذخیره‌شده (یادآورها) هم حذف شوند؟ [y/N]: " confirm
if [[ $confirm == [yY] ]]; then
    rm -rf "$HOME/.config/glass-reminder"
    echo -e "${GREEN}✅ داده‌ها نیز حذف شدند${NC}"
fi

echo -e "${GREEN}✅ حذف کامل انجام شد${NC}"
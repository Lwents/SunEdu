#!/bin/bash

# Script check file .env nào đang chạy trên EC2
# Chạy script này TRÊN SERVER EC2

echo "======================================"
echo "🔍 Kiểm tra .env đang chạy trên Server"
echo "======================================"
echo ""

if [ ! -d "/var/www/SunEdu/backend" ]; then
    echo "❌ Script này phải chạy trên EC2 server"
    echo "Path: /var/www/SunEdu/backend không tồn tại"
    exit 1
fi

cd /var/www/SunEdu/backend

echo "📂 Các file .env có sẵn:"
echo "--------------------------------------"
ls -lah .env* 2>/dev/null | grep -v ".pyc"
echo ""

echo "📄 File .env ĐANG SỬ DỤNG:"
echo "--------------------------------------"
if [ -f ".env" ]; then
    echo "✅ File: .env"
    echo "📊 Size: $(du -h .env | cut -f1)"
    echo "🕐 Modified: $(stat -c %y .env 2>/dev/null || stat -f "%Sm" .env)"
    echo ""
    
    echo "📋 Nội dung (20 dòng đầu):"
    echo "--------------------------------------"
    head -20 .env
    echo "--------------------------------------"
    echo ""
    
    echo "🔑 Các giá trị quan trọng:"
    echo "--------------------------------------"
    grep -E "^(SECRET_KEY|DEBUG|DB_PASSWORD|ALLOWED_HOSTS|FRONTEND_URL)=" .env | sed 's/=.*/=***HIDDEN***/'
    echo ""
else
    echo "❌ File .env KHÔNG TỒN TẠI!"
    echo ""
fi

echo "🔄 Nguồn gốc .env:"
echo "--------------------------------------"

# Check GitHub secret
if grep -q "Updated .env from GitHub secrets" /var/log/syslog 2>/dev/null || \
   grep -q "Updated .env from GitHub secrets" ~/.bash_history 2>/dev/null; then
    echo "📌 Nguồn: GitHub Secret (BACKEND_ENV_FILE)"
    echo "   Priority: 1 (Cao nhất)"
elif [ -f ".env.production" ]; then
    echo "📌 Nguồn: .env.production (từ Git)"
    echo "   Priority: 2"
    
    if [ -f ".env.local.override" ]; then
        echo "   + Merged với: .env.local.override"
        echo ""
        echo "📄 File .env.local.override:"
        echo "--------------------------------------"
        cat .env.local.override
        echo "--------------------------------------"
    fi
else
    echo "📌 Nguồn: .env cũ (giữ nguyên)"
    echo "   Priority: 3"
fi

echo ""
echo "======================================"
echo "💡 KHUYẾN NGHỊ"
echo "======================================"
echo ""

if [ -f ".env.production" ]; then
    echo "✅ Có .env.production - Tự động update khi deploy"
    echo ""
    echo "So sánh .env hiện tại với .env.production:"
    if diff .env .env.production >/dev/null 2>&1; then
        echo "✅ .env giống hệt .env.production"
    else
        echo "⚠️  .env KHÁC với .env.production"
        echo ""
        echo "Xem khác biệt:"
        echo "diff .env .env.production"
    fi
else
    echo "⚠️  Không có .env.production"
    echo "→ Cần pull code mới: git pull origin main"
fi

echo ""

if [ -f ".env.local.override" ]; then
    echo "✅ Có .env.local.override - Overrides được áp dụng"
else
    echo "ℹ️  Không có .env.local.override"
    echo "→ Nếu cần override passwords, tạo file này:"
    echo "   ./server_env_setup.sh (chọn option 2)"
fi

echo ""
echo "======================================"

#!/bin/bash

# Script setup .env trên EC2 server
# Chạy script này TRÊN SERVER EC2

echo "======================================"
echo "🚀 Server Environment Setup"
echo "======================================"
echo ""

# Check if running on server
if [ ! -d "/var/www/SunEdu" ]; then
    echo "❌ Không tìm thấy /var/www/SunEdu"
    echo "Script này phải chạy trên EC2 server"
    exit 1
fi

cd /var/www/SunEdu/backend

echo "📋 Chọn phương thức cấu hình:"
echo ""
echo "1) Tự động dùng .env.production từ Git (Khuyến nghị)"
echo "2) Tạo .env.local.override cho server-specific values"
echo "3) Tạo .env hoàn toàn mới"
echo ""
read -p "Chọn (1-3): " choice

case $choice in
    1)
        if [ -f ".env.production" ]; then
            cp .env.production .env
            chmod 600 .env
            echo ""
            echo "✅ Đã tạo .env từ .env.production"
            echo ""
            echo "⚠️  LƯU Ý: File này sẽ tự động update khi deploy!"
            echo "Nếu cần override giá trị, dùng option 2"
        else
            echo "❌ Không tìm thấy .env.production"
            echo "Pull code mới: git pull origin main"
        fi
        ;;
        
    2)
        if [ ! -f ".env.local.override.example" ]; then
            echo "❌ Không tìm thấy .env.local.override.example"
            exit 1
        fi
        
        if [ -f ".env.local.override" ]; then
            echo "⚠️  File .env.local.override đã tồn tại"
            read -p "Ghi đè? (y/n): " overwrite
            if [ "$overwrite" != "y" ]; then
                echo "Hủy bỏ"
                exit 0
            fi
        fi
        
        cp .env.local.override.example .env.local.override
        chmod 600 .env.local.override
        
        echo ""
        echo "✅ Đã tạo .env.local.override"
        echo ""
        echo "📝 Chỉnh sửa file:"
        echo "nano .env.local.override"
        echo ""
        echo "Thêm các giá trị cần override, ví dụ:"
        echo "DB_PASSWORD=your-secure-password"
        echo "EMAIL_HOST_PASSWORD=your-app-password"
        echo ""
        read -p "Mở editor ngay? (y/n): " edit
        if [ "$edit" = "y" ]; then
            nano .env.local.override
        fi
        
        # Create .env from production + override
        if [ -f ".env.production" ]; then
            cp .env.production .env
            if [ -f ".env.local.override" ]; then
                echo "" >> .env
                echo "# Overrides from .env.local.override" >> .env
                cat .env.local.override >> .env
            fi
            chmod 600 .env
            echo ""
            echo "✅ Đã merge .env.production + .env.local.override"
        fi
        ;;
        
    3)
        if [ -f ".env" ]; then
            echo "⚠️  File .env đã tồn tại"
            read -p "Backup và tạo mới? (y/n): " backup
            if [ "$backup" = "y" ]; then
                mv .env .env.backup.$(date +%Y%m%d_%H%M%S)
                echo "✅ Đã backup .env"
            else
                echo "Hủy bỏ"
                exit 0
            fi
        fi
        
        if [ -f ".env.production" ]; then
            cp .env.production .env
        elif [ -f ".env.example" ]; then
            cp .env.example .env
        else
            echo "❌ Không tìm thấy template .env"
            exit 1
        fi
        
        chmod 600 .env
        
        echo ""
        echo "✅ Đã tạo .env mới"
        echo ""
        echo "📝 QUAN TRỌNG: Chỉnh sửa file .env:"
        echo "nano .env"
        echo ""
        echo "Cần thay đổi:"
        echo "- SECRET_KEY"
        echo "- DB_PASSWORD"
        echo "- EMAIL_HOST_PASSWORD"
        echo "- ALLOWED_HOSTS"
        echo ""
        read -p "Mở editor ngay? (y/n): " edit
        if [ "$edit" = "y" ]; then
            nano .env
        fi
        ;;
        
    *)
        echo "❌ Lựa chọn không hợp lệ"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo "✅ SETUP HOÀN TẤT"
echo "======================================"
echo ""
echo "Kiểm tra cấu hình:"
echo "grep -E '^(DEBUG|SECRET_KEY|DB_PASSWORD|ALLOWED_HOSTS)=' .env"
echo ""
echo "Test deployment:"
echo "docker compose -f docker-compose.prod.yml up -d"
echo ""

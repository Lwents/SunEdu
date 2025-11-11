#!/bin/bash

# Script để switch giữa local và production environment

echo "======================================"
echo "🔄 Environment Switcher"
echo "======================================"
echo ""
echo "Chọn môi trường:"
echo "1) Local Development (DEBUG=True)"
echo "2) Production (DEBUG=False)"
echo "3) Xem file .env hiện tại"
echo "4) Thoát"
echo ""
read -p "Nhập lựa chọn (1-4): " choice

case $choice in
    1)
        if [ -f ".env.local" ]; then
            cp .env.local .env
            echo "✅ Đã chuyển sang môi trường LOCAL"
            echo ""
            echo "📝 Thông tin:"
            echo "- DEBUG: True"
            echo "- Database: localhost:5432"
            echo "- Frontend: http://localhost:5173"
            echo ""
            echo "🚀 Khởi động với:"
            echo "docker compose up -d"
        else
            echo "❌ Không tìm thấy file .env.local"
        fi
        ;;
    2)
        if [ -f ".env.production" ]; then
            echo "⚠️  CẢNH BÁO: Bạn đang chuyển sang môi trường PRODUCTION"
            echo ""
            read -p "Đã kiểm tra và cập nhật DB_PASSWORD chưa? (y/n): " confirm
            if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                cp .env.production .env
                echo "✅ Đã chuyển sang môi trường PRODUCTION"
                echo ""
                echo "📝 Thông tin:"
                echo "- DEBUG: False"
                echo "- Domains: api.smartedu.click, api.smarledu.click"
                echo "- HTTPS enabled"
                echo ""
                echo "🚀 Khởi động với:"
                echo "docker compose -f docker-compose.prod.yml up -d --build"
                echo ""
                echo "⚠️  Checklist:"
                echo "- [ ] DB_PASSWORD đã đổi mạnh hơn"
                echo "- [ ] Email App Password đã cập nhật"
                echo "- [ ] MOMO webhook endpoint hoạt động"
                echo "- [ ] SSL certificate đã cài đặt"
            else
                echo "❌ Hủy bỏ. Hãy cập nhật DB_PASSWORD trước!"
            fi
        else
            echo "❌ Không tìm thấy file .env.production"
        fi
        ;;
    3)
        if [ -f ".env" ]; then
            echo "📄 Nội dung file .env hiện tại:"
            echo "======================================"
            cat .env | grep -E "^(DEBUG|DB_HOST|ALLOWED_HOSTS|FRONTEND_URL)=" | sed 's/^/  /'
            echo "======================================"
        else
            echo "❌ Không tìm thấy file .env"
            echo "Chạy lại script và chọn option 1 hoặc 2"
        fi
        ;;
    4)
        echo "👋 Tạm biệt!"
        exit 0
        ;;
    *)
        echo "❌ Lựa chọn không hợp lệ"
        exit 1
        ;;
esac

echo ""
echo "======================================"

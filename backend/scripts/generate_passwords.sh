#!/bin/bash

# Script để tạo passwords mạnh

echo "======================================"
echo "🔐 Password Generator"
echo "======================================"
echo ""
echo "Chọn loại password cần tạo:"
echo "1) Django SECRET_KEY"
echo "2) Database Password"
echo "3) Cả hai"
echo ""
read -p "Nhập lựa chọn (1-3): " choice

generate_secret_key() {
    if command -v python3 &> /dev/null; then
        echo "Sử dụng Django's get_random_secret_key..."
        SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 2>/dev/null)
        if [ -z "$SECRET_KEY" ]; then
            echo "Django chưa được cài đặt, sử dụng openssl..."
            SECRET_KEY=$(openssl rand -base64 50 | tr -d '\n')
        fi
    else
        echo "Python3 chưa được cài đặt, sử dụng openssl..."
        SECRET_KEY=$(openssl rand -base64 50 | tr -d '\n')
    fi
    echo "✅ SECRET_KEY mới:"
    echo ""
    echo "SECRET_KEY=$SECRET_KEY"
}

generate_db_password() {
    # Tạo password 24 ký tự với chữ hoa, chữ thường, số và ký tự đặc biệt
    DB_PASS=$(openssl rand -base64 32 | tr -d '\n' | head -c 24)
    echo "✅ Database Password mới:"
    echo ""
    echo "DB_PASSWORD=$DB_PASS"
}

echo ""

case $choice in
    1)
        generate_secret_key
        ;;
    2)
        generate_db_password
        ;;
    3)
        generate_secret_key
        echo ""
        echo "======================================"
        echo ""
        generate_db_password
        ;;
    *)
        echo "❌ Lựa chọn không hợp lệ"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo "📝 Hướng dẫn:"
echo "======================================"
echo "1. Copy các giá trị trên"
echo "2. Mở file .env hoặc .env.production"
echo "3. Thay thế các dòng tương ứng"
echo "4. Lưu file"
echo "5. Restart Docker containers"
echo ""
echo "⚠️  LƯU Ý:"
echo "- KHÔNG chia sẻ passwords này"
echo "- KHÔNG commit file .env lên Git"
echo "- Backup passwords an toàn"
echo ""

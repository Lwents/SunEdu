#!/bin/bash

# Script để tạo SECRET_KEY cho Django

echo "======================================"
echo "🔐 Django SECRET_KEY Generator"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 chưa được cài đặt!"
    exit 1
fi

# Generate SECRET_KEY
echo "Đang tạo SECRET_KEY mới..."
echo ""

SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

echo "✅ SECRET_KEY mới của bạn:"
echo ""
echo "SECRET_KEY=$SECRET_KEY"
echo ""
echo "======================================"
echo "📝 Hướng dẫn sử dụng:"
echo "======================================"
echo "1. Copy SECRET_KEY ở trên"
echo "2. Mở file .env"
echo "3. Thay thế dòng SECRET_KEY=..."
echo "4. KHÔNG BAO GIỜ chia sẻ key này!"
echo ""

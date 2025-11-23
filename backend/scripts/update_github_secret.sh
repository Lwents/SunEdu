#!/bin/bash

# Script tự động copy .env.production và tạo hướng dẫn update GitHub Secret

echo "======================================"
echo "🔐 Update GitHub Secret Helper"
echo "======================================"
echo ""

if [ ! -f ".env.production" ]; then
    echo "❌ Không tìm thấy file .env.production"
    exit 1
fi

echo "📋 Nội dung file .env.production:"
echo "======================================"
cat .env.production
echo "======================================"
echo ""

echo "📝 Các bước update GitHub Secret:"
echo ""
echo "1. Copy TOÀN BỘ nội dung trên (từ SECRET_KEY đến cuối)"
echo ""
echo "2. Vào GitHub repository:"
echo "   https://github.com/Lwents/SunEdu/settings/secrets/actions"
echo ""
echo "3. Tìm secret 'BACKEND_ENV_FILE':"
echo "   - Nếu đã có: Click [Update]"
echo "   - Nếu chưa có: Click [New repository secret]"
echo "     Name: BACKEND_ENV_FILE"
echo ""
echo "4. Paste nội dung đã copy vào ô 'Secret'"
echo ""
echo "5. Click [Add secret] hoặc [Update secret]"
echo ""
echo "✅ Xong! Lần deploy tiếp theo sẽ dùng config mới"
echo ""
echo "======================================"
echo "💡 TIP: Copy nội dung bằng cách:"
echo "======================================"
echo ""
echo "# Trên Linux/Mac:"
echo "cat .env.production | xclip -selection clipboard"
echo ""
echo "# Hoặc:"
echo "cat .env.production"
echo "# Rồi Ctrl+Shift+C để copy từ terminal"
echo ""
echo "# Trên Windows (Git Bash):"
echo "cat .env.production | clip"
echo ""

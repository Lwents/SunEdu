#!/bin/bash

# Script tự động update .env.production và trigger deploy
# Chạy trên máy local

echo "======================================"
echo "🔄 Auto Update Production .env"
echo "======================================"
echo ""

cd "$(dirname "$0")"

if [ ! -f ".env.production" ]; then
    echo "❌ Không tìm thấy .env.production"
    exit 1
fi

echo "📝 Chọn thao tác:"
echo ""
echo "1) Update giá trị cụ thể (interactive)"
echo "2) Update từ file .env.local (copy config)"
echo "3) Chỉ update ALLOWED_HOSTS và domains"
echo "4) Xem diff với version hiện tại"
echo "5) Commit và deploy ngay"
echo ""
read -p "Chọn (1-5): " choice

case $choice in
    1)
        echo ""
        echo "📝 Update giá trị cụ thể"
        echo "======================================"
        echo ""
        
        # Backup
        cp .env.production .env.production.backup
        
        echo "Nhập key cần update (ví dụ: DEBUG, DB_PASSWORD):"
        read key
        
        echo "Nhập giá trị mới:"
        read value
        
        # Update value
        if grep -q "^${key}=" .env.production; then
            sed -i "s|^${key}=.*|${key}=${value}|" .env.production
            echo "✅ Đã update ${key}"
        else
            echo "❌ Không tìm thấy ${key}"
            exit 1
        fi
        ;;
        
    2)
        echo ""
        echo "⚠️  Copy config từ .env.local sang .env.production?"
        echo "Điều này sẽ GHI ĐÈ .env.production!"
        read -p "Tiếp tục? (y/n): " confirm
        
        if [ "$confirm" = "y" ]; then
            cp .env.production .env.production.backup
            cp .env.local .env.production
            
            # Update lại một số giá trị cho production
            sed -i 's/DEBUG=True/DEBUG=False/' .env.production
            sed -i 's|http://localhost:5173|https://www.smartedu.click|' .env.production
            
            echo "✅ Đã copy và adjust cho production"
        fi
        ;;
        
    3)
        echo ""
        echo "📝 Update domains và hosts"
        echo "======================================"
        
        cp .env.production .env.production.backup
        
        echo "Nhập ALLOWED_HOSTS (comma-separated):"
        echo "Ví dụ: api.smartedu.click,api.smarledu.click"
        read hosts
        
        sed -i "s|^ALLOWED_HOSTS=.*|ALLOWED_HOSTS=${hosts}|" .env.production
        
        echo ""
        echo "Nhập FRONTEND_URL:"
        echo "Ví dụ: https://www.smartedu.click"
        read frontend
        
        sed -i "s|^FRONTEND_URL=.*|FRONTEND_URL=${frontend}|" .env.production
        
        echo "✅ Đã update domains"
        ;;
        
    4)
        echo ""
        echo "📊 So sánh với Git version:"
        echo "======================================"
        git diff .env.production
        echo ""
        echo "📊 So sánh với .env.local:"
        echo "======================================"
        diff -u .env.local .env.production | head -50
        exit 0
        ;;
        
    5)
        echo ""
        echo "🚀 Commit và deploy"
        echo "======================================"
        
        # Show diff
        echo "Thay đổi:"
        git diff .env.production
        
        echo ""
        read -p "Commit với message: " message
        
        if [ -z "$message" ]; then
            message="Update production environment config"
        fi
        
        git add .env.production
        git commit -m "$message"
        git push origin main
        
        echo ""
        echo "✅ Đã push! Workflow sẽ tự động deploy"
        echo "📊 Xem tiến trình: https://github.com/Lwents/SunEdu/actions"
        exit 0
        ;;
        
    *)
        echo "❌ Lựa chọn không hợp lệ"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo "📋 Xem thay đổi:"
echo "======================================"
git diff .env.production

echo ""
read -p "Commit và deploy ngay? (y/n): " deploy

if [ "$deploy" = "y" ]; then
    read -p "Commit message: " message
    
    if [ -z "$message" ]; then
        message="Update production environment config"
    fi
    
    git add .env.production
    git commit -m "$message"
    git push origin main
    
    echo ""
    echo "✅ Đã deploy! Kiểm tra workflow:"
    echo "https://github.com/Lwents/SunEdu/actions"
else
    echo ""
    echo "💾 Thay đổi đã được lưu vào .env.production"
    echo "Commit thủ công:"
    echo "  git add .env.production"
    echo "  git commit -m 'Update config'"
    echo "  git push origin main"
fi

echo ""
echo "======================================"

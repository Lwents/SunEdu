#!/bin/bash

# Script kiểm tra PostgreSQL trên EC2
# Chạy trên server EC2 để debug database connection

echo "======================================"
echo "🔍 Kiểm tra PostgreSQL trên EC2"
echo "======================================"
echo ""

echo "1️⃣ Kiểm tra PostgreSQL service:"
echo "--------------------------------------"
sudo systemctl status postgresql || echo "❌ PostgreSQL service không chạy"
echo ""

echo "2️⃣ Kiểm tra PostgreSQL đang listen port nào:"
echo "--------------------------------------"
sudo netstat -plnt | grep postgres || sudo ss -plnt | grep postgres || echo "❌ PostgreSQL không listen port nào"
echo ""

echo "3️⃣ Kiểm tra port 5432:"
echo "--------------------------------------"
sudo lsof -i :5432 || echo "❌ Không có process nào listen port 5432"
echo ""

echo "4️⃣ Kiểm tra PostgreSQL version:"
echo "--------------------------------------"
psql --version || echo "❌ psql command không có"
echo ""

echo "5️⃣ Thử connect PostgreSQL:"
echo "--------------------------------------"
sudo -u postgres psql -c "SELECT version();" 2>&1 || echo "❌ Không thể connect PostgreSQL"
echo ""

echo "6️⃣ Kiểm tra database 'elearning':"
echo "--------------------------------------"
sudo -u postgres psql -c "\l" | grep elearning || echo "⚠️  Database 'elearning' không tồn tại"
echo ""

echo "7️⃣ Kiểm tra user 'elearning':"
echo "--------------------------------------"
sudo -u postgres psql -c "\du" | grep elearning || echo "⚠️  User 'elearning' không tồn tại"
echo ""

echo "======================================"
echo "💡 HƯỚNG DẪN FIX"
echo "======================================"
echo ""

# Check nếu service không chạy
if ! systemctl is-active --quiet postgresql 2>/dev/null; then
    echo "🔧 PostgreSQL service KHÔNG chạy!"
    echo ""
    echo "→ Start service:"
    echo "   sudo systemctl start postgresql"
    echo "   sudo systemctl enable postgresql"
    echo ""
fi

# Check nếu database không tồn tại
if ! sudo -u postgres psql -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw elearning; then
    echo "🔧 Database 'elearning' CHƯA TỒN TẠI!"
    echo ""
    echo "→ Tạo database:"
    echo "   sudo -u postgres psql -c \"CREATE DATABASE elearning;\""
    echo "   sudo -u postgres psql -c \"CREATE USER elearning WITH PASSWORD '123456';\""
    echo "   sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE elearning TO elearning;\""
    echo ""
fi

echo "======================================"
echo "🧪 Test Connection"
echo "======================================"
echo ""
echo "→ Test từ command line:"
echo "   PGPASSWORD='123456' psql -h 127.0.0.1 -p 5432 -U elearning -d elearning -c 'SELECT 1;'"
echo ""

echo "======================================"

#!/bin/bash

# Auto fix script for EC2 - Run this from your local machine
# Usage: ./auto_fix_ec2.sh

SSH_KEY="$HOME/Documents/importanr/lwent.pem"
EC2_HOST="ubuntu@3.26.183.143"
PROJECT_PATH="/var/www/SunEdu/backend"

echo "🚀 Starting automatic fix for EC2..."
echo ""

# Fix SSH key permissions
chmod 400 "$SSH_KEY"

# Run all commands on EC2
ssh -i "$SSH_KEY" "$EC2_HOST" << 'ENDSSH'
echo "📂 Moving to project directory..."
cd /var/www/SunEdu/backend

echo ""
echo "� Fixing .env file..."
# Backup file .env
sudo cp .env .env.backup.$(date +%Y%m%d_%H%M%S)

# Sửa ALLOWED_HOSTS - thêm api.smartedu.click
sudo sed -i 's/ALLOWED_HOSTS=smartedu.click,www.smartedu.click,127.0.0.1,localhost/ALLOWED_HOSTS=127.0.0.1,localhost,api.smartedu.click,smartedu.click,www.smartedu.click/' .env

# Sửa CSRF_TRUSTED_ORIGINS - thêm api.smartedu.click
sudo sed -i 's|CSRF_TRUSTED_ORIGINS=https://smartedu.click,https://www.smartedu.click|CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click|' .env

# Sửa CORS_ALLOWED_ORIGINS - thêm api.smartedu.click
sudo sed -i 's|CORS_ALLOWED_ORIGINS=https://smartedu.click,https://www.smartedu.click|CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click|' .env

echo "✅ File .env đã được sửa!"
echo ""
echo "Kiểm tra lại:"
cat .env | grep -E 'ALLOWED_HOSTS|CSRF_TRUSTED|CORS_ALLOWED'

echo ""
echo "🔄 Restarting Docker containers..."
sudo docker compose -f docker-compose.prod.yml down
sudo docker compose -f docker-compose.prod.yml up -d

echo ""
echo "⏳ Waiting 30 seconds for containers to start..."
sleep 30

echo ""
echo "📊 Checking container status..."
sudo docker compose -f docker-compose.prod.yml ps

echo ""
echo "📝 Checking logs..."
sudo docker compose -f docker-compose.prod.yml logs --tail=30 web

echo ""
echo "✅ Done! Please check if the website is working:"
echo "   - Frontend: https://smartedu.click"
echo "   - API: https://api.smartedu.click/admin/"
ENDSSH

echo ""
echo "🎉 Fix completed!"


#!/bin/bash

# Script to copy .env content for GitHub Secret
# This will display the .env content that you need to copy to GitHub Secret BACKEND_ENV_FILE

echo "=================================================="
echo "📋 COPY NỘI DUNG DƯỚI ĐÂY VÀO GITHUB SECRET"
echo "=================================================="
echo ""
echo "Secret name: BACKEND_ENV_FILE"
echo "Repository: https://github.com/Lwents/SunEdu/settings/secrets/actions"
echo ""
echo "=================================================="
echo ""

cat backend/.env

echo ""
echo "=================================================="
echo "✅ Copy toàn bộ nội dung phía trên"
echo "=================================================="
echo ""
echo "Các bước:"
echo "1. Vào: https://github.com/Lwents/SunEdu/settings/secrets/actions"
echo "2. Tìm secret 'BACKEND_ENV_FILE'"
echo "3. Click 'Update'"
echo "4. Paste nội dung đã copy"
echo "5. Click 'Update secret'"
echo ""


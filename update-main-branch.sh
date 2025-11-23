#!/bin/bash
# Script để update branch main sau khi tắt protection rules

echo "🚀 Updating main branch..."

cd /home/lwent/Documents/SunEdu || exit 1

# Fetch latest
echo "📥 Fetching latest code..."
git fetch origin develop main

# Checkout main locally
echo "🌿 Checking out main branch..."
git checkout main 2>/dev/null || git checkout -b main origin/main

# Reset to develop (clean code)
echo "🔄 Resetting main to develop (clean code)..."
git reset --hard origin/develop

# Push to main
echo "📤 Pushing to main..."
git push origin main --force

echo ""
echo "✅ Done! Main branch đã được update."
echo ""
echo "Bây giờ bạn có thể:"
echo "1. Bật lại protection rules trên GitHub"
echo "2. Kiểm tra: git log origin/main --oneline -3"

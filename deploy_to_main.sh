#!/bin/bash

# Script to merge develop to main and trigger deployment

set -e

echo "🚀 Deploying to main branch..."
echo ""

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Current branch: $CURRENT_BRANCH"

# Checkout[object Object]Switching to main branch..."
git checkout main

# Pull latest
echo "📥 Pulling latest main..."
git pull origin main

# Merge develop
echo "🔀 Merging develop into main..."
git merge develop --no-edit -m "Merge develop: Fix disk space and optimize deployment"

# Push to trigger deployment
echo "📤 Pushing to GitHub (will trigger auto-deploy)..."
git push origin main

echo ""
echo "✅ Done! Deployment triggered."
echo ""
echo "📊 Monitor deployment at:"
echo "   https://github.com/Lwents/SunEdu/actions"
echo ""
echo "💡 If deployment fails due to disk space:"
echo "   1. SSH to EC2: ssh ec2-user@your-ec2-ip"
echo "   2. Run: cd /var/www/SunEdu/backend && bash fix_disk_space_now.sh"
echo "   3. Retry deployment from GitHub Actions"
echo ""

# Switch back to original branch
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "🔙 Switching back to $CURRENT_BRANCH..."
    git checkout "$CURRENT_BRANCH"
fi

echo "✅ All done!"


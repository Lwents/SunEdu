#!/bin/bash

# Script to clean up EC2 disk space
# Run this manually on EC2 if disk is full

set -e

echo "🧹 EC2 Disk Cleanup Script"
echo "=========================="
echo ""

# Show current disk usage
echo "📊 Current disk usage:"
df -h /
echo ""

# Clean Docker
echo "🐳 Cleaning Docker system..."
docker system prune -af --volumes || true
docker builder prune -af || true
echo "✅ Docker cleaned"
echo ""

# Clean old Docker images
echo "[object Object]Removing old Docker images..."
docker images | grep '<none>' | awk '{print $3}' | xargs -r docker rmi -f || true
docker images | grep 'sunedu' | tail -n +3 | awk '{print $3}' | xargs -r docker rmi -f || true
echo "✅ Old images removed"
echo ""

# Clean Python cache
echo "🐍 Cleaning Python cache..."
find /var/www/SunEdu -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find /var/www/SunEdu -type f -name "*.pyc" -delete 2>/dev/null || true
find /var/www/SunEdu -type f -name "*.pyo" -delete 2>/dev/null || true
rm -rf ~/.cache/pip/* || true
echo "✅ Python cache cleaned"
echo ""

# Clean apt cache
echo "📦 Cleaning apt cache..."
sudo apt-get clean || true
sudo apt-get autoclean || true
sudo apt-get autoremove -y || true
sudo rm -rf /var/lib/apt/lists/* || true
echo "✅ Apt cache cleaned"
echo ""

# Clean logs (keep last 7 days)
echo "📝 Cleaning old logs..."
find /var/log -type f -name "*.log" -mtime +7 -delete 2>/dev/null || true
find /var/www/SunEdu -type f -name "*.log" -size +100M -exec truncate -s 0 {} \; 2>/dev/null || true
echo "✅ Old logs cleaned"
echo ""

# Clean systemd journal
echo "📰 Cleaning systemd journal..."
sudo journalctl --vacuum-time=7d || true
sudo journalctl --vacuum-size=100M || true
echo "✅ Journal cleaned"
echo ""

# Clean temporary files
echo "🗑️  Cleaning temporary files..."
sudo rm -rf /tmp/* 2>/dev/null || true
sudo rm -rf /var/tmp/* 2>/dev/null || true
echo "✅ Temporary files cleaned"
echo ""

# Show final disk usage
echo "📊 Final disk usage:"
df -h /
echo ""

# Show largest directories
echo "📊 Top 10 largest directories in /var/www/SunEdu:"
du -h /var/www/SunEdu 2>/dev/null | sort -rh | head -10 || true
echo ""

echo "✅ Cleanup complete!"
echo ""
echo "💡 Tips:"
echo "  - Run this script regularly to prevent disk space issues"
echo "  - Consider increasing EC2 instance disk size if needed"
echo "  - Monitor disk usage with: df -h"
echo "  - Check Docker disk usage with: docker system df"


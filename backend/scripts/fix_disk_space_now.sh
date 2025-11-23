#!/bin/bash

# Emergency script to fix disk space issues on EC2
# Run this immediately if deployment fails due to disk space

set -e

echo "🚨 EMERGENCY DISK SPACE FIX"
echo "==========================="
echo ""

# Show current disk usage
echo "📊 Current disk usage:"
df -h /
echo ""

# Check if disk is critically full (>90%)
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 90 ]; then
    echo "✅ Disk usage is ${DISK_USAGE}% - not critical"
    echo "   But we'll clean up anyway..."
    echo ""
fi

# Stop running containers first to free up resources
echo "🛑 Stopping running containers..."
cd /var/www/SunEdu/backend
docker compose -f docker-compose.prod.yml down --volumes --remove-orphans 2>/dev/null || true
docker compose -f docker-compose.yml down --volumes --remove-orphans 2>/dev/null || true
echo "✅ Containers stopped"
echo ""

# Aggressive Docker cleanup
echo "🐳 AGGRESSIVE Docker cleanup..."
docker system prune -af --volumes || true
docker builder prune -af || true
docker volume prune -f || true
docker network prune -f || true

# Remove ALL Docker images (will be rebuilt)
echo "[object Object] Docker images..."
docker rmi -f $(docker images -aq) 2>/dev/null || true
echo "✅ All Docker images removed"
echo ""

# Clean Python cache
echo "🐍 Cleaning Python cache..."
find /var/www/SunEdu -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find /var/www/SunEdu -type f -name "*.pyc" -delete 2>/dev/null || true
find /var/www/SunEdu -type f -name "*.pyo" -delete 2>/dev/null || true
rm -rf ~/.cache/pip/* || true
rm -rf /root/.cache/pip/* 2>/dev/null || true
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

# Truncate large log files
echo "📝 Truncating large log files..."
find /var/log -type f -name "*.log" -size +50M -exec truncate -s 10M {} \; 2>/dev/null || true
find /var/www/SunEdu -type f -name "*.log" -size +50M -exec truncate -s 10M {} \; 2>/dev/null || true
echo "✅ Large logs truncated"
echo ""

# Clean systemd journal
echo "📰 Cleaning systemd journal..."
sudo journalctl --vacuum-time=3d || true
sudo journalctl --vacuum-size=50M || true
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

DISK_USAGE_AFTER=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
FREED=$((DISK_USAGE - DISK_USAGE_AFTER))

echo "✅ Cleanup complete!"
echo "   Freed: ${FREED}% disk space"
echo "   Current usage: ${DISK_USAGE_AFTER}%"
echo ""

if [ "$DISK_USAGE_AFTER" -gt 85 ]; then
    echo "⚠️  WARNING: Disk usage still high (${DISK_USAGE_AFTER}%)"
    echo ""
    echo "💡 Recommendations:"
    echo "   1. Increase EC2 instance disk size"
    echo "   2. Set up swap space: bash setup_swap_ec2.sh"
    echo "   3. Move data to external storage (S3, EBS)"
    echo ""
    echo "📊 Largest directories:"
    du -h /var/www/SunEdu 2>/dev/null | sort -rh | head -5 || true
else
    echo "✅ Disk space is now healthy!"
    echo ""
    echo "🚀 You can now retry the deployment"
fi


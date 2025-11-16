#!/bin/bash

# Script to set up swap space on EC2
# This helps when building Docker images with limited RAM

set -e

SWAP_SIZE_GB=4

echo "💾 Setting up ${SWAP_SIZE_GB}GB swap space on EC2"
echo "=============================================="
echo ""

# Check if swap already exists
if swapon --show | grep -q '/swapfile'; then
    echo "⚠️  Swap already exists:"
    swapon --show
    echo ""
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cancelled"
        exit 0
    fi
    
    echo "🛑 Disabling existing swap..."
    sudo swapoff /swapfile
    sudo rm -f /swapfile
fi

# Create swap file
echo "[object Object]SWAP_SIZE_GB}GB swap file..."
sudo fallocate -l ${SWAP_SIZE_GB}G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1G count=${SWAP_SIZE_GB}

# Set permissions
echo "🔒 Setting permissions..."
sudo chmod 600 /swapfile

# Make swap
echo "⚙️  Setting up swap..."
sudo mkswap /swapfile

# Enable swap
echo "✅ Enabling swap..."
sudo swapon /swapfile

# Make it permanent
if ! grep -q '/swapfile' /etc/fstab; then
    echo "💾 Making swap permanent..."
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# Optimize swap settings
echo "⚙️  Optimizing swap settings..."
sudo sysctl vm.swappiness=10
sudo sysctl vm.vfs_cache_pressure=50

# Make settings permanent
if ! grep -q 'vm.swappiness' /etc/sysctl.conf; then
    echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
fi
if ! grep -q 'vm.vfs_cache_pressure' /etc/sysctl.conf; then
    echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
fi

echo ""
echo "✅ Swap setup complete!"
echo ""
echo "📊 Current memory status:"
free -h
echo ""
echo "📊 Swap status:"
swapon --show
echo ""
echo "💡 Swap is now active and will persist after reboot"


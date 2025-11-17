#!/bin/bash

# Script tự động resize filesystem sau khi tăng EBS volume
# Chạy trên EC2 instance

set -e

echo "================================================"
echo "🔧 EC2 Disk Resize Script"
echo "================================================"
echo ""

# Màu sắc
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Kiểm tra quyền root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Script này cần chạy với sudo${NC}"
    echo "Chạy lại: sudo bash $0"
    exit 1
fi

echo -e "${YELLOW}📊 Tình trạng TRƯỚC khi resize:${NC}"
df -h /
echo ""

# Tìm root device
ROOT_DEVICE=$(findmnt -n -o SOURCE /)
echo -e "${GREEN}✓${NC} Root filesystem: $ROOT_DEVICE"

# Lấy disk device (bỏ partition number)
if [[ $ROOT_DEVICE == *"nvme"* ]]; then
    # NVMe device (newer instances)
    DISK_DEVICE=$(echo $ROOT_DEVICE | sed 's/p[0-9]*$//')
    PARTITION_NUM=$(echo $ROOT_DEVICE | grep -o '[0-9]*$')
else
    # Xen device (older instances)
    DISK_DEVICE=$(echo $ROOT_DEVICE | sed 's/[0-9]*$//')
    PARTITION_NUM=$(echo $ROOT_DEVICE | grep -o '[0-9]*$')
fi

echo -e "${GREEN}✓${NC} Disk device: $DISK_DEVICE"
echo -e "${GREEN}✓${NC} Partition: $PARTITION_NUM"
echo ""

# Hiển thị layout hiện tại
echo -e "${YELLOW}📋 Current disk layout:${NC}"
lsblk
echo ""

# Hỏi xác nhận
read -p "⚠️  Bạn có muốn tiếp tục resize? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Đã hủy."
    exit 0
fi

echo ""
echo -e "${YELLOW}🔄 Bước 1: Mở rộng partition...${NC}"

# Grow partition
if growpart $DISK_DEVICE $PARTITION_NUM; then
    echo -e "${GREEN}✓${NC} Partition đã được mở rộng"
else
    echo -e "${YELLOW}⚠${NC}  Partition có thể đã được mở rộng trước đó"
fi
echo ""

echo -e "${YELLOW}🔄 Bước 2: Resize filesystem...${NC}"

# Kiểm tra filesystem type
FS_TYPE=$(findmnt -n -o FSTYPE /)
echo -e "${GREEN}✓${NC} Filesystem type: $FS_TYPE"

# Resize filesystem dựa trên type
if [ "$FS_TYPE" = "ext4" ] || [ "$FS_TYPE" = "ext3" ]; then
    resize2fs $ROOT_DEVICE
    echo -e "${GREEN}✓${NC} Ext4 filesystem đã được resize"
elif [ "$FS_TYPE" = "xfs" ]; then
    xfs_growfs /
    echo -e "${GREEN}✓${NC} XFS filesystem đã được resize"
else
    echo -e "${RED}❌ Không hỗ trợ filesystem type: $FS_TYPE${NC}"
    exit 1
fi

echo ""
echo "================================================"
echo -e "${GREEN}✅ HOÀN THÀNH!${NC}"
echo "================================================"
echo ""
echo -e "${YELLOW}📊 Tình trạng SAU khi resize:${NC}"
df -h /
echo ""

# Tính toán space tăng thêm
AVAILABLE_GB=$(df -BG / | tail -1 | awk '{print $4}' | sed 's/G//')
if [ $AVAILABLE_GB -gt 5 ]; then
    echo -e "${GREEN}🎉 Thành công! Bạn có $AVAILABLE_GB GB khả dụng${NC}"
else
    echo -e "${YELLOW}⚠️  Cảnh báo: Chỉ còn $AVAILABLE_GB GB. Cần cleanup thêm.${NC}"
fi


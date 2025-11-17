# Hướng dẫn tăng dung lượng ổ cứng EC2

## Tình trạng hiện tại
- **Disk:** 6.8GB (96% full - chỉ còn 307MB!)
- **Cần:** Tăng lên ít nhất 20GB

## Cách 1: Tăng qua AWS Console (Dễ nhất) ⭐

### Bước 1: Vào AWS Console
1. Đăng nhập: https://console.aws.amazon.com/
2. Chọn region: **ap-southeast-2** (Sydney)
3. Vào **EC2 Dashboard**

### Bước 2: Tìm Volume
1. Sidebar trái → **Volumes** (trong mục Elastic Block Store)
2. Tìm volume đang attach vào instance `3.26.183.143`
3. Hoặc lọc theo Instance ID

### Bước 3: Modify Volume
1. Chọn volume → **Actions** → **Modify Volume**
2. Thay đổi **Size** từ `8 GB` → `20 GB` (hoặc 30GB)
3. Click **Modify** → **Yes**
4. Đợi 1-2 phút cho volume resize

### Bước 4: Mở rộng filesystem trên EC2
SSH vào EC2 và chạy:

```bash
# Kiểm tra partition
lsblk

# Mở rộng partition (thường là /dev/xvda1 hoặc /dev/nvme0n1p1)
sudo growpart /dev/xvda 1

# Resize filesystem
sudo resize2fs /dev/xvda1

# Kiểm tra lại
df -h /
```

## Cách 2: Dùng AWS CLI (Nhanh)

```bash
# Lấy Volume ID
VOLUME_ID=$(aws ec2 describe-instances \
  --instance-ids i-YOUR-INSTANCE-ID \
  --query 'Reservations[0].Instances[0].BlockDeviceMappings[0].Ebs.VolumeId' \
  --output text \
  --region ap-southeast-2)

# Tăng size lên 20GB
aws ec2 modify-volume \
  --volume-id $VOLUME_ID \
  --size 20 \
  --region ap-southeast-2

# Đợi hoàn thành
aws ec2 wait volume-in-use \
  --volume-ids $VOLUME_ID \
  --region ap-southeast-2
```

Sau đó SSH vào EC2 và chạy bước 4 ở trên.

## Script tự động (Chạy trên EC2)

Tôi sẽ tạo script để tự động resize sau khi bạn tăng volume từ AWS Console.

## Khuyến nghị

- **Tăng lên:** 20GB (đủ dùng) hoặc 30GB (thoải mái)
- **Chi phí:** ~$2-3/tháng cho 20GB EBS gp3
- **Thời gian:** 5-10 phút tổng cộng

## Sau khi tăng xong

Chạy script cleanup để giải phóng thêm space:
```bash
ssh -i ~/Documents/importanr/lwent.pem ubuntu@3.26.183.143
cd /var/www/SunEdu/backend
bash fix_disk_space_now.sh
```


# ✅ EC2 Bad Request (400) Error - ĐÃ SỬA THÀNH CÔNG!

## 🎉 Kết quả

**Lỗi đã được sửa hoàn toàn!**

- ✅ **API Admin:** https://api.smartedu.click/admin/ - HTTP 302 (Redirect to login) ✓
- ✅ **API Courses:** https://api.smartedu.click/api/content/courses/ - HTTP 200 OK ✓
- ✅ **Frontend:** https://smartedu.click ✓

---

## 🔍 Nguyên nhân lỗi

File `.env` trên EC2 server (`/var/www/SunEdu/backend/.env`) thiếu domain `api.smartedu.click` trong các biến môi trường:

**Trước khi sửa:**
```env
ALLOWED_HOSTS=smartedu.click,www.smartedu.click,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://smartedu.click,https://www.smartedu.click
CORS_ALLOWED_ORIGINS=https://smartedu.click,https://www.smartedu.click
```

**Sau khi sửa:**
```env
ALLOWED_HOSTS=127.0.0.1,localhost,api.smartedu.click,smartedu.click,www.smartedu.click
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click
```

---

## 🛠️ Các bước đã thực hiện

### 1. Kết nối SSH vào EC2
```bash
ssh -i ~/Documents/importanr/lwent.pem ubuntu@3.26.183.143
```

### 2. Tìm thư mục project
- Thư mục project: `/var/www/SunEdu/backend`
- Docker containers đang chạy từ thư mục này

### 3. Sửa file .env
```bash
cd /var/www/SunEdu/backend

# Backup file .env
sudo cp .env .env.backup.20251116_031036

# Sửa ALLOWED_HOSTS
sudo sed -i 's/ALLOWED_HOSTS=smartedu.click,www.smartedu.click,127.0.0.1,localhost/ALLOWED_HOSTS=127.0.0.1,localhost,api.smartedu.click,smartedu.click,www.smartedu.click/' .env

# Sửa CSRF_TRUSTED_ORIGINS
sudo sed -i 's|CSRF_TRUSTED_ORIGINS=https://smartedu.click,https://www.smartedu.click|CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click|' .env

# Sửa CORS_ALLOWED_ORIGINS
sudo sed -i 's|CORS_ALLOWED_ORIGINS=https://smartedu.click,https://www.smartedu.click|CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click|' .env
```

### 4. Restart Docker containers
```bash
sudo docker compose -f docker-compose.prod.yml down
sudo docker compose -f docker-compose.prod.yml up -d
```

### 5. Kiểm tra kết quả
```bash
# Test API Admin
curl -I https://api.smartedu.click/admin/
# Kết quả: HTTP/1.1 302 Found ✓

# Test API Courses
curl -I https://api.smartedu.click/api/content/courses/
# Kết quả: HTTP/1.1 200 OK ✓
```

---

## 📝 Thông tin EC2 Server

- **IP:** 3.26.183.143
- **User:** ubuntu
- **SSH Key:** ~/Documents/importanr/lwent.pem
- **Project Path:** /var/www/SunEdu/backend
- **Docker Compose File:** docker-compose.prod.yml

---

## 🚀 Script tự động

Đã tạo script `auto_fix_ec2.sh` để tự động sửa lỗi trong tương lai:

```bash
cd backend
./auto_fix_ec2.sh
```

Script sẽ tự động:
1. SSH vào EC2
2. Backup file .env
3. Sửa các biến môi trường
4. Restart Docker containers
5. Kiểm tra logs

---

## 📊 Trạng thái hiện tại

**Docker Containers:**
- ✅ backend-db-1 (postgres:15) - Up and healthy
- ✅ backend-web-1 (backend-web) - Up and running on port 8000

**Gunicorn:**
- ✅ 4 workers đang chạy
- ✅ Listening at http://0.0.0.0:8000

**Nginx:**
- ✅ Reverse proxy hoạt động bình thường
- ✅ SSL certificates hoạt động

---

## 🎯 Kết luận

Lỗi Bad Request (400) đã được sửa hoàn toàn bằng cách thêm `api.smartedu.click` vào các biến môi trường trong file `.env` trên EC2 server.

Website hiện đang hoạt động bình thường:
- Frontend: https://smartedu.click
- API: https://api.smartedu.click
- Admin: https://api.smartedu.click/admin/

---

**Ngày sửa:** 16/11/2025  
**Thời gian:** 03:11 UTC  
**Người thực hiện:** Augment Agent


# 🚀 Hướng dẫn sửa lỗi Bad Request (400) trên EC2 - NHANH

## ⚡ Cách nhanh nhất (Từ máy local)

```bash
cd backend
./deploy_fix_to_ec2.sh ~/.ssh/your-key.pem ubuntu@your-ec2-ip
```

**Thay thế:**
- `~/.ssh/your-key.pem` → Đường dẫn đến SSH key của bạn
- `ubuntu@your-ec2-ip` → User và IP của EC2 server

Script sẽ tự động:
1. ✅ Kết nối SSH vào EC2
2. ✅ Pull code mới nhất từ develop
3. ✅ Chạy script sửa lỗi .env
4. ✅ Restart Docker containers
5. ✅ Kiểm tra logs

---

## 🔧 Cách thủ công (SSH vào server)

### Bước 1: SSH vào EC2
```bash
ssh -i ~/.ssh/your-key.pem ubuntu@your-ec2-ip
```

### Bước 2: Di chuyển vào thư mục project
```bash
cd /home/ubuntu/SunEdu/backend
```

### Bước 3: Pull code mới
```bash
git pull origin develop
```

### Bước 4: Chạy script sửa lỗi
```bash
chmod +x fix_env_on_server.sh
./fix_env_on_server.sh
```

### Bước 5: Restart containers
```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d
```

### Bước 6: Kiểm tra
```bash
# Xem logs
docker compose -f docker-compose.prod.yml logs -f web

# Kiểm tra containers
docker compose -f docker-compose.prod.yml ps
```

---

## 🐛 Nguyên nhân lỗi

File `.env` trên server có lỗi chính tả:
- ❌ `api.smarledu.click` (thiếu chữ 't')
- ✅ `api.smartedu.click` (đúng)

Django từ chối request vì domain không khớp với cấu hình.

---

## ✅ Kiểm tra sau khi sửa

1. **Truy cập Admin:**
   ```bash
   curl -I https://api.smartedu.click/admin/
   ```
   Kết quả mong đợi: HTTP 200 hoặc 302

2. **Truy cập Frontend:**
   - https://smartedu.click

3. **Kiểm tra API:**
   ```bash
   curl https://api.smartedu.click/api/content/courses/
   ```

---

## 📚 Tài liệu chi tiết

- [FIX_EC2_ERROR.md](./FIX_EC2_ERROR.md) - Hướng dẫn chi tiết đầy đủ
- [fix_env_on_server.sh](./fix_env_on_server.sh) - Script sửa lỗi trên server
- [deploy_fix_to_ec2.sh](./deploy_fix_to_ec2.sh) - Script deploy từ local

---

## 🆘 Nếu vẫn lỗi

1. Kiểm tra logs chi tiết:
   ```bash
   docker compose -f docker-compose.prod.yml logs --tail=100 web
   ```

2. Kiểm tra file .env:
   ```bash
   cat .env | grep -E "ALLOWED_HOSTS|CSRF|CORS"
   ```

3. Restart lại containers:
   ```bash
   docker compose -f docker-compose.prod.yml restart
   ```

4. Nếu vẫn không được, rebuild:
   ```bash
   docker compose -f docker-compose.prod.yml down
   docker compose -f docker-compose.prod.yml up -d --build
   ```


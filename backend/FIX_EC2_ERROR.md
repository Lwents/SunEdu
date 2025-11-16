# Hướng dẫn sửa lỗi Bad Request (400) trên EC2

## Nguyên nhân lỗi

File `.env` trên server EC2 có lỗi chính tả trong các domain:
- `api.smarledu.click` (thiếu chữ 't') → Nên là `api.smartedu.click`
- `smarledu.click` (thiếu chữ 't') → Nên là `smartedu.click`

Django từ chối request vì domain không khớp với `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, và `CORS_ALLOWED_ORIGINS`.

## Cách sửa

### Cách 1: Sử dụng script tự động (Khuyến nghị)

1. SSH vào EC2:
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

2. Di chuyển vào thư mục backend:
```bash
cd /path/to/SunEdu/backend
```

3. Pull code mới nhất từ develop:
```bash
git pull origin develop
```

4. Chạy script sửa lỗi:
```bash
chmod +x fix_env_on_server.sh
./fix_env_on_server.sh
```

5. Restart Docker containers:
```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d
```

6. Kiểm tra logs:
```bash
docker compose -f docker-compose.prod.yml logs -f web
```

### Cách 2: Sửa thủ công

1. SSH vào EC2 và mở file `.env`:
```bash
cd /path/to/SunEdu/backend
nano .env
```

2. Sửa các dòng sau:

**Trước:**
```env
ALLOWED_HOSTS=127.0.0.1,localhost,api.smartedu.click,api.smarledu.click
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://api.smarledu.click,https://www.smarledu.click,https://smartedu.click
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,https://smartedu.click,https://www.smartedu.click,https://smarledu.click,https://www.smarledu.click
```

**Sau:**
```env
ALLOWED_HOSTS=127.0.0.1,localhost,api.smartedu.click
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,https://smartedu.click,https://www.smartedu.click
```

3. Lưu file (Ctrl+O, Enter, Ctrl+X)

4. Restart Docker containers:
```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d
```

## Kiểm tra sau khi sửa

1. Kiểm tra containers đang chạy:
```bash
docker compose -f docker-compose.prod.yml ps
```

2. Kiểm tra logs:
```bash
docker compose -f docker-compose.prod.yml logs -f web
```

3. Test API:
```bash
curl -I https://api.smartedu.click/admin/
```

Kết quả mong đợi: HTTP 200 hoặc 302 (redirect to login)

4. Truy cập website:
- Frontend: https://smartedu.click
- API: https://api.smartedu.click
- Admin: https://api.smartedu.click/admin/

## Lưu ý

- File `.env` không được commit lên git vì chứa thông tin nhạy cảm
- Mỗi lần deploy, cần đảm bảo file `.env` trên server có cấu hình đúng
- Nên tạo backup của file `.env` trước khi sửa


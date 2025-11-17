# 🚀 Deployment Guide

## Quick Deploy

### 1. Chuẩn bị môi trường

```bash
# Copy file cấu hình mẫu
cp .env.production.example .env

# Chỉnh sửa file .env với thông tin thực tế
nano .env
```

**Các biến quan trọng cần thay đổi:**
- `SECRET_KEY`: Generate key mới với `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `DB_PASSWORD`: Mật khẩu database mạnh
- `EMAIL_HOST_USER` và `EMAIL_HOST_PASSWORD`: Thông tin email SMTP
- `MOMO_*`: Thông tin MoMo payment gateway (nếu dùng)

### 2. Deploy

```bash
# Chạy script deploy tự động
./deploy.sh
```

Script sẽ tự động:
- ✅ Kiểm tra file .env
- ✅ Tạo các thư mục cần thiết
- ✅ Pull code mới nhất (nếu có git)
- ✅ Build Docker images
- ✅ Start services
- ✅ Kiểm tra health

### 3. Kiểm tra

```bash
# Xem logs
docker compose logs -f web

# Kiểm tra status
docker compose ps

# Test API
curl http://localhost:8000/api/content/courses/
```

## Manual Deploy

Nếu không dùng script tự động:

```bash
# 1. Tạo thư mục
mkdir -p logs runtime_logs media staticfiles
chmod 777 logs runtime_logs media

# 2. Build và start
docker compose down
docker compose build --no-cache
docker compose up -d

# 3. Kiểm tra
docker compose logs -f web
```

## Cấu hình Production

### Docker Compose

File `docker-compose.yml` đã được cấu hình với:
- ✅ PostgreSQL 15 với health check
- ✅ Redis 7 Alpine với health check
- ✅ Django web service với health check
- ✅ Auto-restart on failure
- ✅ Volume persistence cho database và Redis

### Environment Variables

**Required:**
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Danh sách domains
- `CSRF_TRUSTED_ORIGINS`: Danh sách origins cho CSRF
- `CORS_ALLOWED_ORIGINS`: Danh sách origins cho CORS
- `DB_*`: Database credentials
- `REDIS_HOST`, `REDIS_PORT`: Redis connection

**Optional:**
- `EMAIL_*`: Email SMTP settings
- `MOMO_*`: Payment gateway settings
- `OPENAI_API_KEY`: AI features

## Troubleshooting

### Lỗi Redis Connection

Nếu gặp lỗi "Connection refused" với Redis:

```bash
# Kiểm tra Redis đang chạy
docker compose ps redis

# Kiểm tra .env có đúng không
grep REDIS .env

# Phải có:
# REDIS_HOST=redis
# REDIS_PORT=6379
```

### Lỗi CORS

Nếu frontend không kết nối được API:

```bash
# Kiểm tra CORS settings trong .env
grep CORS .env

# Phải bao gồm tất cả domains:
# CORS_ALLOWED_ORIGINS=https://smartedu.click,https://www.smartedu.click,https://api.smartedu.click
```

### Lỗi 500 Internal Server Error

```bash
# Xem logs chi tiết
docker compose logs --tail=100 web

# Kiểm tra migrations
docker compose exec web python manage.py showmigrations

# Chạy migrations nếu cần
docker compose exec web python manage.py migrate
```

### Lỗi Permission Denied

```bash
# Cấp quyền cho thư mục logs
chmod 777 logs runtime_logs media
```

## Backup & Restore

### Backup Database

```bash
docker compose exec db pg_dump -U elearning elearning > backup_$(date +%Y%m%d).sql
```

### Restore Database

```bash
cat backup_20231117.sql | docker compose exec -T db psql -U elearning elearning
```

## Monitoring

```bash
# Xem logs realtime
docker compose logs -f

# Xem logs của service cụ thể
docker compose logs -f web
docker compose logs -f db
docker compose logs -f redis

# Kiểm tra resource usage
docker stats
```

## Updates

Khi có code mới:

```bash
# Pull code
git pull origin develop

# Rebuild và restart
./deploy.sh
```

Hoặc manual:

```bash
git pull origin develop
docker compose down
docker compose build --no-cache
docker compose up -d
```

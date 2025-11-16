# Hướng dẫn chạy Backend bằng Docker

## Cấu trúc Docker

Project sử dụng Docker Compose với 3 services:
- **web**: Django backend server (port 8000)
- **db**: PostgreSQL database (port 5433)
- **redis**: Redis cache/broker (port 6379)

## Các lệnh cơ bản

### 1. Khởi động services
```bash
cd /home/lwent/Documents/SunEdu/backend
docker-compose up -d
```

### 2. Build lại images (khi có thay đổi code)
```bash
docker-compose up -d --build
```

### 3. Xem logs
```bash
# Xem logs của tất cả services
docker-compose logs -f

# Xem logs của service cụ thể
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f redis
```

### 4. Dừng services
```bash
docker-compose stop
```

### 5. Dừng và xóa containers
```bash
docker-compose down
```

### 6. Dừng và xóa containers + volumes (xóa data)
```bash
docker-compose down -v
```

### 7. Xem trạng thái
```bash
docker-compose ps
```

## Chạy lệnh trong container

### Django management commands
```bash
# Migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Django shell
docker-compose exec web python manage.py shell

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Database commands
```bash
# PostgreSQL shell
docker-compose exec db psql -U elearning -d elearning
```

## Truy cập services

- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **PostgreSQL**: localhost:5433
  - Database: elearning
  - User: elearning
  - Password: 123456
- **Redis**: localhost:6379

## Environment Variables

Các biến môi trường được định nghĩa trong:
- `.env` file (được load bởi docker-compose)
- `docker-compose.yml` (environment section)

## Troubleshooting

### 1. Port đã được sử dụng
```bash
# Kiểm tra port đang được sử dụng
sudo lsof -i :8000
sudo lsof -i :5433
sudo lsof -i :6379

# Hoặc thay đổi port trong docker-compose.yml
```

### 2. Database connection error
```bash
# Kiểm tra database đã sẵn sàng chưa
docker-compose logs db

# Chạy migrations lại
docker-compose exec web python manage.py migrate
```

### 3. Rebuild containers
```bash
# Xóa containers và build lại
docker-compose down
docker-compose up -d --build
```

### 4. Xem logs lỗi
```bash
# Xem logs chi tiết
docker-compose logs web --tail=100

# Xem logs real-time
docker-compose logs -f web
```

## Production

Để chạy production, sử dụng `docker-compose.prod.yml`:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Notes

- Code được mount vào container, nên thay đổi code sẽ được reflect ngay (không cần rebuild)
- Database data được lưu trong volume `postgres_data`
- Redis data được lưu trong volume `redis_data`
- Logs được lưu trong `/app/logs` trong container



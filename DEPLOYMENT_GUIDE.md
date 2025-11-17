# 🚀 Hướng dẫn Deploy tự động qua GitHub Actions

## ⚠️ BẢO MẬT - QUAN TRỌNG

**KHÔNG BAO GIỜ** commit các file sau vào Git:
- ❌ File `.env` 
- ❌ File chứa password, API keys, secrets
- ❌ File có tên chứa `SECRET`, `PASSWORD`, `KEY`, `CREDENTIALS`

## 📝 Cấu hình GitHub Secrets

### Bước 1: Truy cập GitHub Secrets

1. Mở repository: https://github.com/Lwents/SunEdu
2. Vào **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** hoặc **Edit** secret hiện có

### Bước 2: Tạo/Cập nhật secret `BACKEND_ENV_FILE`

**Tên secret:** `BACKEND_ENV_FILE`

**Nội dung:** Copy file `.env` production của bạn (KHÔNG commit file này vào Git!)

**Các biến BẮT BUỘC phải có:**

```bash
# Django Core
SECRET_KEY=<your-secret-key>
DEBUG=False

# Database
DB_NAME=elearning
DB_USER=elearning
DB_PASSWORD=<your-db-password>
DB_HOST=db
DB_PORT=5432

# Domains - QUAN TRỌNG: Phải có đủ 3 domains
ALLOWED_HOSTS=api.smartedu.click,smartedu.click,www.smartedu.click,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://smartedu.click,https://www.smartedu.click,https://api.smartedu.click
CORS_ALLOWED_ORIGINS=https://smartedu.click,https://www.smartedu.click,https://api.smartedu.click
FRONTEND_URL=https://smartedu.click

# Redis - QUAN TRỌNG: Bắt buộc phải có
REDIS_HOST=redis
REDIS_PORT=6379

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_USE_SSL=false
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<your-app-password>
DEFAULT_FROM_EMAIL=SmartEdu <<your-email>>

# Payment Gateway (optional)
MOMO_PARTNER_CODE=<your-partner-code>
MOMO_ACCESS_KEY=<your-access-key>
MOMO_SECRET_KEY=<your-secret-key>
MOMO_PARTNER_NAME=<your-partner-name>
MOMO_STORE_ID=<your-store-id>
MOMO_CREATE_ENDPOINT=https://test-payment.momo.vn/v2/gateway/api/create
MOMO_POS_ENDPOINT=https://test-payment.momo.vn/v2/gateway/api/pos
MOMO_REDIRECT_URL=https://smartedu.click/student/payments
MOMO_IPN_URL=https://smartedu.click/api/payments/momo/ipn/
```

### Bước 3: Kiểm tra các secrets khác

Đảm bảo có đủ 4 secrets:
- ✅ `BACKEND_ENV_FILE` - File .env cho backend
- ✅ `EC2_HOST` - IP của EC2 server
- ✅ `EC2_USERNAME` - SSH username (thường là `ubuntu`)
- ✅ `EC2_SSH_KEY` - Private SSH key (nội dung file .pem)

## 🚀 Cách Deploy

### Deploy tự động (Recommended)

Khi push code lên branch `develop` hoặc `main`, GitHub Actions sẽ tự động deploy:

```bash
git add .
git commit -m "your changes"
git push origin develop
```

Workflow sẽ tự động:
1. ✅ Pull code mới
2. ✅ Tạo file `.env` từ GitHub secret
3. ✅ Tự động thêm REDIS config nếu thiếu
4. ✅ Tự động thêm api.smartedu.click vào CORS/CSRF nếu thiếu
5. ✅ Build Docker images
6. ✅ Start services
7. ✅ Health check

### Deploy thủ công

Vào **Actions** tab → **Deploy Backend** → **Run workflow** → Chọn branch → **Run workflow**

## ✅ Kiểm tra deployment

### 1. Xem logs trên GitHub

- Vào **Actions** tab
- Click vào workflow run mới nhất
- Xem logs chi tiết từng step

### 2. Xem logs trên server

```bash
ssh -i <your-key.pem> ubuntu@<your-ec2-ip>
cd /home/ubuntu/SunEdu/backend
docker compose logs -f web
```

### 3. Test API

```bash
curl https://api.smartedu.click/api/content/courses/
```

## 🔧 Troubleshooting

### Lỗi: "No .env configuration found"

→ Kiểm tra secret `BACKEND_ENV_FILE` đã được tạo chưa

### Lỗi: CORS blocked

→ Đảm bảo `CORS_ALLOWED_ORIGINS` có đủ 3 domains:
- https://smartedu.click
- https://www.smartedu.click
- https://api.smartedu.click

### Lỗi: Redis connection refused

→ Đảm bảo có 2 biến:
- REDIS_HOST=redis
- REDIS_PORT=6379

### Lỗi: 500 Internal Server Error

→ Xem logs chi tiết:
```bash
docker compose logs --tail=100 web
```

## 📊 Workflow Features

### Auto-fix Configuration

Workflow tự động sửa các vấn đề phổ biến:

1. **Thiếu Redis config** → Tự động thêm `REDIS_HOST=redis` và `REDIS_PORT=6379`
2. **Thiếu api.smartedu.click trong CORS** → Tự động thêm vào `CORS_ALLOWED_ORIGINS`
3. **Thiếu api.smartedu.click trong CSRF** → Tự động thêm vào `CSRF_TRUSTED_ORIGINS`
4. **Thiếu thư mục logs** → Tự động tạo `logs`, `runtime_logs`, `media`

### Deployment Path

- ✅ Code location: `/home/ubuntu/SunEdu`
- ✅ Docker Compose: `docker-compose.yml` hoặc `docker-compose.prod.yml`
- ✅ Services: PostgreSQL, Redis, Django web

## 🎯 Best Practices

1. ✅ **Luôn dùng GitHub Secrets** cho thông tin nhạy cảm
2. ✅ **Không commit file .env** vào Git
3. ✅ **Test trên develop** trước khi merge vào main
4. ✅ **Xem logs** sau mỗi lần deploy
5. ✅ **Backup database** định kỳ

## 📝 Checklist trước khi deploy

- [ ] Đã cập nhật `BACKEND_ENV_FILE` secret với đầy đủ config
- [ ] File `.env` có `REDIS_HOST=redis` và `REDIS_PORT=6379`
- [ ] CORS/CSRF có đủ 3 domains (bao gồm api.smartedu.click)
- [ ] Code đã được test trên local
- [ ] Đã commit và push code
- [ ] Đã kiểm tra GitHub Actions logs

## 🔐 Security Notes

**QUAN TRỌNG:**
- 🔒 File `.env` đã được thêm vào `.gitignore`
- 🔒 Mọi file có tên chứa `SECRET`, `PASSWORD`, `KEY` sẽ bị ignore
- 🔒 Chỉ dùng GitHub Secrets để lưu thông tin nhạy cảm
- 🔒 Không bao giờ hardcode passwords trong code

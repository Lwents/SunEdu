# 🔐 Hướng dẫn cập nhật GitHub Secret BACKEND_ENV_FILE

## ⚠️ VẤN ĐỀ

Mỗi lần deploy, GitHub Actions sẽ ghi đè file `.env` trên EC2 từ secret `BACKEND_ENV_FILE`.

Nếu secret này thiếu `api.smartedu.click`, sau mỗi lần deploy sẽ lại bị lỗi Bad Request (400).

## 📋 NỘI DUNG SECRET CẦN CẬP NHẬT

Copy toàn bộ nội dung dưới đây và paste vào GitHub Secret `BACKEND_ENV_FILE`:

```env
# ==============================================
# DJANGO CORE SETTINGS
# ==============================================

# SECRET_KEY - ĐÃ CẬP NHẬT KEY MỚI MẠNH HƠN
SECRET_KEY=your-secret-key-here-change-this-in-production

# DEBUG - ĐỂ False KHI DEPLOY PRODUCTION
DEBUG=False

# ==============================================
# DATABASE SETTINGS
# ==============================================
DB_NAME=elearning
DB_USER=elearning
# ⚠️ CẢNH BÁO: Đổi password này khi deploy production!
# Khuyến nghị: password ít nhất 16 ký tự, có chữ hoa, số, ký tự đặc biệt
DB_PASSWORD=your-strong-db-password-here
DB_HOST=db
DB_PORT=5432

# ==============================================
# ALLOWED HOSTS (comma-separated, no spaces)
# ==============================================
ALLOWED_HOSTS=127.0.0.1,localhost,api.smartedu.click

# ==============================================
# CSRF TRUSTED ORIGINS (comma-separated, no spaces)
# ⚠️ LƯU Ý: Đã loại bỏ http:// cho production URLs
# ==============================================
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click

# ==============================================
# CORS ALLOWED ORIGINS (comma-separated, no spaces)
# ⚠️ ĐÃ LOẠI BỎ http:// cho production domains (chỉ dùng https://)
# ==============================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click

# ==============================================
# FRONTEND SETTINGS
# ==============================================
FRONTEND_URL=https://smartedu.click

# ==============================================
# MOMO PAYMENT GATEWAY
# ⚠️ LƯU Ý: Đây là test credentials, thay bằng production keys khi go-live
# ==============================================
MOMO_PARTNER_CODE=YOUR_MOMO_PARTNER_CODE
MOMO_ACCESS_KEY=YOUR_MOMO_ACCESS_KEY
MOMO_SECRET_KEY=YOUR_MOMO_SECRET_KEY
MOMO_REDIRECT_URL=https://smartedu.click/payment/callback
MOMO_IPN_URL=https://api.smartedu.click/api/payments/momo/ipn/
MOMO_ENDPOINT=https://test-payment.momo.vn/v2/gateway/api/create

# ==============================================
# CELERY SETTINGS
# ==============================================
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# ==============================================
# EMAIL SETTINGS
# ==============================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password-here
DEFAULT_FROM_EMAIL=noreply@smartedu.click

# ==============================================
# AWS S3 SETTINGS (Optional)
# ==============================================
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=ap-southeast-1
```

## 🔧 CÁCH CẬP NHẬT

### Bước 1: Truy cập GitHub Settings

1. Vào repository: https://github.com/Lwents/SunEdu
2. Click **Settings** (tab phía trên)
3. Trong sidebar bên trái, click **Secrets and variables** → **Actions**

### Bước 2: Cập nhật Secret

1. Tìm secret `BACKEND_ENV_FILE` trong danh sách
2. Click nút **Edit** (biểu tượng bút chì)
3. Xóa nội dung cũ
4. Copy toàn bộ nội dung từ phần "NỘI DUNG SECRET CẦN CẬP NHẬT" ở trên
5. Paste vào ô **Value**
6. Click **Update secret**

### Bước 3: Deploy lại

Sau khi cập nhật secret, deploy lại:

**Cách 1: Push code mới**

```bash
git add .
git commit -m "Update .env configuration"
git push origin develop
```

**Cách 2: Chạy workflow thủ công**

1. Vào tab **Actions** trên GitHub
2. Click workflow **Deploy Backend**
3. Click **Run workflow**
4. Chọn branch `develop`
5. Click **Run workflow**

## ✅ KIỂM TRA SAU KHI DEPLOY

```bash
# Test API Admin
curl -I https://api.smartedu.click/admin/
# Kết quả mong đợi: HTTP/1.1 302 Found

# Test API Courses
curl -I https://api.smartedu.click/api/content/courses/
# Kết quả mong đợi: HTTP/1.1 200 OK
```

## 📝 LƯU Ý QUAN TRỌNG

1. **Không commit file `.env` lên git** - File này chứa thông tin nhạy cảm
2. **Luôn cập nhật GitHub Secret khi thay đổi cấu hình** - Nếu không, mỗi lần deploy sẽ ghi đè lại
3. **Backup secret trước khi sửa** - Copy nội dung cũ ra file text để phòng trường hợp cần rollback

## 🔍 KIỂM TRA SECRET HIỆN TẠI

Để xem secret hiện tại trên EC2:

```bash
ssh -i ~/Documents/importanr/lwent.pem ubuntu@3.26.183.143 "cat /var/www/SunEdu/backend/.env | grep -E 'ALLOWED_HOSTS|CSRF_TRUSTED|CORS_ALLOWED'"
```

Kết quả mong đợi:

```
ALLOWED_HOSTS=127.0.0.1,localhost,api.smartedu.click
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click
```

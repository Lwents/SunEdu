# 🔐 Hướng dẫn cập nhật GitHub Secrets

## Bước 1: Cập nhật BACKEND_ENV_FILE

1. Mở GitHub repository: https://github.com/Lwents/SunEdu
2. Vào **Settings** → **Secrets and variables** → **Actions**
3. Tìm secret `BACKEND_ENV_FILE` và click **Edit** (hoặc **New repository secret** nếu chưa có)
4. Copy toàn bộ nội dung file `GITHUB_SECRET_BACKEND_ENV_FILE.txt` và paste vào
5. Click **Update secret**

## Nội dung cần paste (đã sửa đầy đủ):

```
SECRET_KEY=b2+UZvatIff7eTI9+6hVKCq1QrrWxVkBE12r2XVgN7CCqoy7ESgKYKgP1tOo827yNAU=
DEBUG=False

DB_NAME=elearning
DB_USER=elearning
DB_PASSWORD=123456
DB_HOST=db
DB_PORT=5432

ALLOWED_HOSTS=api.smartedu.click,smartedu.click,www.smartedu.click,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://smartedu.click,https://www.smartedu.click,https://api.smartedu.click
CORS_ALLOWED_ORIGINS=https://smartedu.click,https://www.smartedu.click,https://api.smartedu.click
FRONTEND_URL=https://smartedu.click

REDIS_HOST=redis
REDIS_PORT=6379

MOMO_PARTNER_CODE=MOMO
MOMO_ACCESS_KEY=F8BBA842ECF85
MOMO_SECRET_KEY=K951B6PE1waDMi640xX08PD3vg6EkVlz
MOMO_PARTNER_NAME=MOMO
MOMO_STORE_ID=Store001
MOMO_CREATE_ENDPOINT=https://test-payment.momo.vn/v2/gateway/api/create
MOMO_POS_ENDPOINT=https://test-payment.momo.vn/v2/gateway/api/pos
MOMO_REDIRECT_URL=https://smartedu.click/student/payments
MOMO_IPN_URL=https://smartedu.click/api/payments/momo/ipn/

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_USE_SSL=false
EMAIL_HOST_USER=kiritovn777@gmail.com
EMAIL_HOST_PASSWORD=asiznulbltdqhdiy
DEFAULT_FROM_EMAIL=SmartEdu <kiritovn777@gmail.com>
```

## ✅ Những gì đã được sửa so với file cũ:

1. ✅ **Thêm REDIS_HOST=redis** - Fix lỗi Redis connection
2. ✅ **Thêm REDIS_PORT=6379** - Fix lỗi Redis connection
3. ✅ **Thêm https://api.smartedu.click vào CORS_ALLOWED_ORIGINS** - Fix CORS error
4. ✅ **Thêm https://api.smartedu.click vào CSRF_TRUSTED_ORIGINS** - Fix CSRF error

## Bước 2: Kiểm tra các secrets khác

Đảm bảo có đủ các secrets sau:
- ✅ `BACKEND_ENV_FILE` - File .env cho backend (vừa cập nhật)
- ✅ `EC2_HOST` - IP của EC2 (3.26.183.143)
- ✅ `EC2_USERNAME` - Username SSH (ubuntu)
- ✅ `EC2_SSH_KEY` - Private key SSH (lwent.pem)

## Bước 3: Test deployment

Sau khi cập nhật secret:

```bash
# Push code lên develop
git push origin develop

# Workflow sẽ tự động chạy và deploy lên EC2
```

Hoặc trigger manual:
1. Vào **Actions** tab
2. Chọn workflow **Deploy Backend**
3. Click **Run workflow**
4. Chọn branch **develop**
5. Click **Run workflow**

## 🎯 Kết quả sau khi deploy

✅ Không còn lỗi CORS  
✅ Không còn lỗi Redis connection  
✅ Admin dashboard hoạt động (không còn 500 error)  
✅ Tất cả API endpoints hoạt động  

## 🔍 Kiểm tra logs

Xem logs của GitHub Actions:
1. Vào **Actions** tab
2. Click vào workflow run mới nhất
3. Xem logs chi tiết

Xem logs trên server:
```bash
ssh -i lwent.pem ubuntu@3.26.183.143
cd /home/ubuntu/SunEdu/backend
docker compose logs -f web
```

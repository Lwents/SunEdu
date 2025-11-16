# 📝 Hướng dẫn sử dụng file .env

## 📂 Các file đã tạo:

### 1. `.env.local` - Cho môi trường Local Development
- DEBUG = True
- Dùng localhost URLs
- Test Momo credentials
- Webhook.site cho testing

### 2. `.env.production` - Cho môi trường Production (EC2)
- DEBUG = False  
- Dùng production domains (smartedu.click, smarledu.click)
- HTTPS URLs
- Production webhook URLs

## 🔧 Cách sử dụng:

### Local Development:
```bash
# Copy file local
cp .env.local .env

# Khởi động Docker
docker compose up -d
```

### Production (EC2):
```bash
# Copy file production
cp .env.production .env

# Chỉnh sửa các giá trị cần thiết
nano .env

# Khởi động với production config
docker compose -f docker-compose.prod.yml up -d --build
```

## ⚠️ QUAN TRỌNG - Các điều cần làm trước khi deploy:

### 1. ✅ SECRET_KEY đã được cập nhật
- Đã tạo key mới mạnh: `b2+UZvatIff7eTI9+6hVKCq1QrrWxVkBE12r2XVgN7CCqoy7ESgKYKgP1tOo827yNAU=`

### 2. ⚠️ DB_PASSWORD vẫn yếu
**Cần thay đổi ngay:**
```bash
# Tạo password mạnh
openssl rand -base64 32

# Hoặc dùng password generator với:
# - Ít nhất 16 ký tự
# - Có chữ hoa, chữ thường, số, ký tự đặc biệt
# Ví dụ: Str0ng!P@ssw0rd#2024$Elearn
```

### 3. ⚠️ Email Password đang lộ
**Nên sử dụng App Password thay vì password thật:**
1. Vào https://myaccount.google.com/apppasswords
2. Tạo App Password mới cho "Mail"
3. Thay `majrjbsmnmluzwdo` bằng App Password 16 ký tự mới
4. **KHÔNG BAO GIỜ** commit password thật lên Git

### 4. ⚠️ Momo IPN URL cần cập nhật
Trong `.env.production`, đã đổi:
```
# Từ:
MOMO_IPN_URL=https://webhook.site/7eab3452-46cc-49a9-991f-93d2146f2cd7

# Thành:
MOMO_IPN_URL=https://api.smartedu.click/api/payments/momo-webhook/
```
**Cần đảm bảo endpoint này hoạt động trên server!**

## 🔒 Bảo mật:

### File .gitignore đã được tạo để bảo vệ:
- `.env`
- `.env.local`
- `.env.production`
- `.env.*.local`

### Kiểm tra xem .env đã bị track chưa:
```bash
git status
# Nếu thấy .env trong danh sách, chạy:
git rm --cached .env
git rm --cached .env.local
git rm --cached .env.production
```

## 📊 So sánh các thay đổi:

| Mục | Trước | Sau | Status |
|-----|-------|-----|--------|
| SECRET_KEY | `dev-secret-elearing` | `b2+UZvat...` (50 chars) | ✅ Fixed |
| DEBUG | `True` | `False` (production) | ✅ Fixed |
| DB_PASSWORD | `123456` | `123456` | ⚠️ Cần đổi |
| ALLOWED_HOSTS | Có localhost + domains | Tách riêng local/prod | ✅ Improved |
| CORS Origins | Có cả http/https | Prod chỉ https | ✅ Improved |
| FRONTEND_URL | localhost | Prod domain | ✅ Fixed |
| MOMO_IPN_URL | webhook.site | API endpoint | ✅ Fixed |

## 🚀 Checklist Deploy:

- [x] Tạo SECRET_KEY mới
- [x] Tách file .env cho local/production  
- [x] Cấu hình DEBUG=False cho production
- [x] Cập nhật CORS/CSRF cho production domains
- [x] Cập nhật MOMO IPN URL
- [ ] **ĐỔI DB_PASSWORD MẠNH HƠN**
- [ ] **DÙNG EMAIL APP PASSWORD**
- [ ] Test local với .env.local
- [ ] Deploy lên EC2 với .env.production
- [ ] Verify tất cả endpoints hoạt động

## 💡 Tips:

### Để test nhanh local:
```bash
# Dùng file local
cp .env.local .env
docker compose up -d
```

### Để deploy production:
```bash
# Dùng file production
cp .env.production .env

# ĐỔI DB_PASSWORD TRƯỚC KHI CHẠY!
nano .env

# Deploy
docker compose -f docker-compose.prod.yml up -d --build
```

## 📞 Lưu ý quan trọng:

1. **KHÔNG BAO GIỜ** commit file `.env` lên Git
2. **LUÔN LUÔN** dùng `.env.production` khi deploy
3. **THAY ĐỔI** DB_PASSWORD trước khi deploy production
4. **SỬ DỤNG** App Password cho Gmail
5. **KIỂM TRA** MOMO webhook endpoint hoạt động
6. **BACKUP** database trước khi migrate

## 🆘 Nếu gặp lỗi:

### "Bad Request (400)"
→ Kiểm tra ALLOWED_HOSTS có đúng domain/IP không

### "CSRF verification failed"  
→ Kiểm tra CSRF_TRUSTED_ORIGINS có https:// và đúng domain

### "CORS error"
→ Kiểm tra CORS_ALLOWED_ORIGINS và đảm bảo frontend domain đúng

### "Email sending failed"
→ Kiểm tra EMAIL_HOST_PASSWORD là App Password, không phải password Gmail

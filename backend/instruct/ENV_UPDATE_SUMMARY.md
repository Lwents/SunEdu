# 📋 TÓM TẮT CẬP NHẬT FILE .ENV

## ✅ ĐÃ HOÀN THÀNH

### 1. Tạo SECRET_KEY mới mạnh
- **Trước:** `dev-secret-elearing` (yếu, dễ đoán)
- **Sau:** `b2+UZvatIff7eTI9+6hVKCq1QrrWxVkBE12r2XVgN7CCqoy7ESgKYKgP1tOo827yNAU=`
- **Độ dài:** 68 ký tự, random base64

### 2. Tạo file .env tách biệt
✅ `.env.local` - Cho Local Development
- DEBUG = True
- localhost URLs
- Test credentials

✅ `.env.production` - Cho Production EC2
- DEBUG = False
- Production domains (smartedu.click, smarledu.click)
- HTTPS URLs
- Production webhook endpoints

### 3. Cải thiện cấu hình

#### CORS & CSRF
**Trước:** Lẫn lộn http và https
**Sau:** 
- Local: Chỉ http://localhost
- Production: Chỉ https:// cho production domains

#### FRONTEND_URL
**Trước:** `http://localhost:5173` (cả local và prod)
**Sau:**
- Local: `http://localhost:5173`
- Production: `https://www.smartedu.click`

#### MOMO_IPN_URL
**Trước:** `https://webhook.site/...` (test URL)
**Sau:**
- Local: Giữ webhook.site (để test)
- Production: `https://api.smartedu.click/api/payments/momo-webhook/`

### 4. Tạo Scripts hỗ trợ

✅ `switch_env.sh` - Switch giữa local/production
```bash
./switch_env.sh
```

✅ `generate_passwords.sh` - Tạo passwords mạnh
```bash
./generate_passwords.sh
```

✅ `generate_secret_key.sh` - Tạo Django SECRET_KEY
```bash
./generate_secret_key.sh
```

### 5. Tạo Documentation

✅ `ENV_GUIDE.md` - Hướng dẫn sử dụng chi tiết
✅ `ENV_UPDATE_SUMMARY.md` - File này

## ⚠️ CẦN LÀM TIẾP

### 1. ĐỔI DB_PASSWORD (CRITICAL!)
**Hiện tại:** `123456` - QUÁ YẾU!
**Cần làm:**
```bash
# Tạo password mới
./generate_passwords.sh

# Hoặc dùng
openssl rand -base64 32

# Cập nhật vào .env.production
nano .env.production
```

### 2. CẬP NHẬT EMAIL APP PASSWORD
**Hiện tại:** Đang dùng password Gmail trực tiếp - KHÔNG AN TOÀN!
**Cần làm:**
1. Vào https://myaccount.google.com/apppasswords
2. Tạo App Password mới cho "Mail"
3. Cập nhật `EMAIL_HOST_PASSWORD` trong .env

### 3. VERIFY MOMO WEBHOOK
**Đảm bảo endpoint này hoạt động:**
```
https://api.smartedu.click/api/payments/momo-webhook/
```

## 🚀 CÁCH SỬ DỤNG

### Local Development:
```bash
# 1. Switch sang local
./switch_env.sh
# Chọn option 1

# 2. Khởi động
docker compose up -d

# 3. Truy cập
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

### Production Deployment:
```bash
# 1. ĐỔI DB_PASSWORD TRƯỚC!
nano .env.production
# Thay DB_PASSWORD=123456 bằng password mạnh

# 2. Cập nhật EMAIL_HOST_PASSWORD
# Thay bằng App Password từ Google

# 3. Switch sang production
./switch_env.sh
# Chọn option 2

# 4. Deploy
docker compose -f docker-compose.prod.yml up -d --build

# 5. Verify
curl https://api.smartedu.click/admin/
```

## 📊 SO SÁNH TRƯỚC/SAU

| Cấu hình | Trước | Sau (Local) | Sau (Production) |
|----------|-------|-------------|------------------|
| SECRET_KEY | dev-secret (yếu) | strong-key | strong-key |
| DEBUG | True | True | **False** |
| DB_PASSWORD | 123456 | 123456 | **⚠️ Cần đổi** |
| ALLOWED_HOSTS | Lẫn lộn | localhost | Production domains |
| CORS | http + https | http://localhost | https://domains |
| FRONTEND_URL | localhost | localhost | https://smartedu.click |
| MOMO_IPN | webhook.site | webhook.site | API endpoint |

## 🔒 SECURITY CHECKLIST

- [x] SECRET_KEY đã đổi mạnh
- [x] DEBUG=False trong production
- [x] Tách file .env local/production
- [x] CORS/CSRF cấu hình đúng
- [ ] **DB_PASSWORD cần đổi mạnh hơn**
- [ ] **EMAIL_HOST_PASSWORD dùng App Password**
- [x] ALLOWED_HOSTS cấu hình đúng
- [x] Production dùng HTTPS
- [ ] Verify MOMO webhook hoạt động
- [ ] Test đầy đủ trước deploy

## 📁 CẤU TRÚC FILES

```
backend/
├── .env                          # Symlink (tạo bằng switch_env.sh)
├── .env.local                    # ✅ Local development
├── .env.production               # ✅ Production config
├── .env.example                  # Template
├── .gitignore                    # ✅ Bảo vệ .env files
├── docker-compose.yml            # Dev compose
├── docker-compose.prod.yml       # ✅ Production compose
├── Dockerfile                    # ✅ Updated
├── switch_env.sh                 # ✅ Switch environments
├── generate_passwords.sh         # ✅ Generate passwords
├── generate_secret_key.sh        # ✅ Generate SECRET_KEY
├── ENV_GUIDE.md                  # ✅ Hướng dẫn chi tiết
├── ENV_UPDATE_SUMMARY.md         # ✅ File này
├── DEPLOY.md                     # ✅ Deploy guide
├── SECURITY_ISSUES.md            # ✅ Security checklist
└── nginx.conf.example            # ✅ Nginx config
```

## ⚡ QUICK START

### Lần đầu setup:
```bash
# 1. Generate passwords mới
./generate_passwords.sh

# 2. Cập nhật .env.production với passwords mới
nano .env.production

# 3. Test local
./switch_env.sh  # Chọn 1
docker compose up -d

# 4. Nếu OK, deploy production
./switch_env.sh  # Chọn 2
docker compose -f docker-compose.prod.yml up -d --build
```

## 🆘 TROUBLESHOOTING

### "Bad Request (400)"
```bash
# Check ALLOWED_HOSTS
grep ALLOWED_HOSTS .env
```

### "CSRF verification failed"
```bash
# Check CSRF_TRUSTED_ORIGINS có https://
grep CSRF_TRUSTED_ORIGINS .env
```

### "Email not sending"
```bash
# Kiểm tra đã dùng App Password chưa
grep EMAIL_HOST_PASSWORD .env
```

## 📞 NEXT STEPS

1. **ĐỌC** `ENV_GUIDE.md` để hiểu chi tiết
2. **ĐỔI** DB_PASSWORD trong `.env.production`
3. **CẬP NHẬT** EMAIL_HOST_PASSWORD với App Password
4. **TEST** local với `.env.local`
5. **DEPLOY** production với `.env.production`
6. **VERIFY** tất cả endpoints hoạt động

---

✅ **Đã sẵn sàng để deploy an toàn hơn!**

⚠️ **Nhớ đổi DB_PASSWORD và EMAIL_HOST_PASSWORD trước khi go-live!**

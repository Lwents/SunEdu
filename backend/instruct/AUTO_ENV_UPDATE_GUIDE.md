# 🔄 Hướng dẫn Tự động Cập nhật .env trên Server

## 🎯 TÓM TẮT - 3 PHƯƠNG ÁN

### ✅ PHƯƠNG ÁN 1: GitHub Secrets (BẢO MẬT NHẤT)

**Workflow đã hỗ trợ sẵn!**

```bash
# Bước 1: Chạy script helper
cd backend
./update_github_secret.sh

# Bước 2: Copy output và update GitHub Secret
# Vào: https://github.com/Lwents/SunEdu/settings/secrets/actions
# Update secret: BACKEND_ENV_FILE
```

**Ưu điểm:**
- ✅ Bảo mật tuyệt đối (secrets không lộ trong code)
- ✅ Dễ update (chỉ cần update secret)
- ✅ Tự động apply khi deploy

**Nhược điểm:**
- ❌ Phải update qua GitHub UI
- ❌ Không xem được nội dung secret sau khi lưu

---

### ✅ PHƯƠNG ÁN 2: .env.production từ Git (KHUYẾN NGHỊ)

**Đã được cài đặt trong workflow!**

**Cách hoạt động:**
1. Commit file `.env.production` vào git
2. Workflow tự động copy `.env.production` → `.env` trên server
3. Tự động update mỗi lần deploy

**Cấu hình:**
```bash
# Trên máy local
cd backend

# File .env.production đã có sẵn và được commit
git add .env.production
git commit -m "Update production config"
git push

# Khi deploy, workflow tự động:
# cp .env.production .env
```

**⚠️ LƯU Ý:**
- File `.env.production` sẽ được commit vào git
- KHÔNG nên để password nhạy cảm trong file này
- Dùng kết hợp với `.env.local.override` cho passwords

**Ưu điểm:**
- ✅ Tự động sync mỗi lần deploy
- ✅ Không cần update GitHub secrets
- ✅ Có thể track changes trong git
- ✅ Dễ rollback

**Nhược điểm:**
- ⚠️ File trong git → có thể bị lộ nếu repo public
- ⚠️ Cần cẩn thận với passwords

---

### ✅ PHƯƠNG ÁN 3: .env.local.override (TỐT NHẤT CHO PASSWORDS)

**Kết hợp PHƯƠNG ÁN 2 + override cho giá trị nhạy cảm**

**Setup trên server:**
```bash
# SSH vào EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Chạy script setup
cd /var/www/SunEdu/backend
./server_env_setup.sh

# Chọn option 2
# Tạo file .env.local.override
```

**File .env.local.override (chỉ tồn tại trên server):**
```bash
# Override DB password
DB_PASSWORD=super-secure-password-only-on-server

# Override Email password
EMAIL_HOST_PASSWORD=app-password-from-google

# Override API keys
OPENAI_API_KEY=sk-real-key-only-on-server
MOMO_SECRET_KEY=real-momo-key
```

**Workflow tự động merge:**
```
.env = .env.production + .env.local.override
```

**Ưu điểm:**
- ✅ Passwords không bao giờ rời khỏi server
- ✅ .env.production chỉ chứa config non-sensitive
- ✅ Tự động merge khi deploy
- ✅ Dễ quản lý

**Nhược điểm:**
- ⚠️ Phải setup lần đầu trên server

---

## 🚀 SETUP CỤ THỂ

### 1️⃣ Setup lần đầu trên Server

```bash
# SSH vào EC2
ssh -i your-key.pem ubuntu@54.xxx.xxx.xxx

# Vào project
cd /var/www/SunEdu/backend

# Pull code mới
git pull origin main

# Chạy script setup
./server_env_setup.sh

# Chọn option 2 (Khuyến nghị)
# Tạo .env.local.override với passwords thật
```

### 2️⃣ Cấu hình .env.local.override

```bash
# Trên EC2 server
nano /var/www/SunEdu/backend/.env.local.override
```

Thêm nội dung:
```bash
# Database - Password mạnh chỉ có trên server
DB_PASSWORD=YourStr0ng!Passw0rd#2024

# Email - App Password từ Google
EMAIL_HOST_PASSWORD=your-16-char-app-password

# MoMo - Production keys
MOMO_ACCESS_KEY=real-production-key
MOMO_SECRET_KEY=real-production-secret

# OpenAI (nếu dùng)
OPENAI_API_KEY=sk-your-real-openai-key
```

Lưu và đóng (Ctrl+X, Y, Enter)

### 3️⃣ Test

```bash
# Test merge
cd /var/www/SunEdu/backend
cat .env | grep DB_PASSWORD

# Should show: DB_PASSWORD=YourStr0ng!Passw0rd#2024
```

---

## 📋 WORKFLOW FLOW

### Khi bạn push code:

```
1. Git Push
   ↓
2. GitHub Actions trigger
   ↓
3. SSH vào EC2
   ↓
4. Git pull origin main
   ↓
5. Tạo .env:
   
   if BACKEND_ENV_FILE secret exists:
     Use secret
   else if .env.production exists:
     Copy .env.production → .env
     
     if .env.local.override exists:
       Merge .env.local.override → .env
   
   ↓
6. Deploy với .env mới
```

---

## 🔒 BẢO MẬT

### ✅ An toàn để commit:
- `.env.production` - Với values mặc định/placeholder
- `.env.example` - Template
- `.env.local.override.example` - Example

### ❌ KHÔNG BAO GIỜ commit:
- `.env` - Active config
- `.env.local.override` - Server overrides
- `.env.local` - Local dev with real data

### File .gitignore đã được update:
```gitignore
.env
.env.local
.env.local.override
.env.*.local
```

---

## 💡 KHUYẾN NGHỊ

### Cho dự án này (SunEdu):

**Dùng kết hợp PHƯƠNG ÁN 2 + 3:**

1. ✅ Commit `.env.production` vào git với:
   - DEBUG=False
   - SECRET_KEY (có thể public, sẽ override)
   - DB_PASSWORD=placeholder
   - Config chung: ALLOWED_HOSTS, CORS, etc.

2. ✅ Tạo `.env.local.override` trên EC2 với:
   - DB_PASSWORD thật
   - EMAIL_HOST_PASSWORD thật
   - API keys thật

3. ✅ Workflow tự động merge mỗi lần deploy

**Kết quả:**
- Config tự động update qua git
- Passwords an toàn trên server
- Không cần update GitHub secrets
- Dễ quản lý và maintain

---

## 🆘 TROUBLESHOOTING

### File .env không tự động update sau deploy?

```bash
# Check workflow logs
# Vào GitHub → Actions → Xem log deploy

# Hoặc check trên server
ssh ubuntu@ec2
cd /var/www/SunEdu/backend
ls -la .env*
cat .env | head -5
```

### .env.local.override không được merge?

```bash
# Check workflow
cd /var/www/SunEdu/backend
ls -la .env.local.override

# Nếu file không tồn tại, tạo mới
./server_env_setup.sh
```

### Muốn thay đổi config ngay lập tức?

```bash
# Option 1: Update .env trực tiếp (tạm thời)
ssh ubuntu@ec2
nano /var/www/SunEdu/backend/.env
sudo systemctl restart sunedu-backend

# Option 2: Update .env.local.override (vĩnh viễn)
nano /var/www/SunEdu/backend/.env.local.override
# Trigger deploy hoặc manual merge
```

---

## 🎯 QUICK START

### Lần đầu setup:

```bash
# 1. Trên máy local - Đảm bảo .env.production đúng
cd backend
cat .env.production

# 2. Push code
git add .env.production
git commit -m "Add production config"
git push origin main

# 3. Trên EC2 - Setup overrides
ssh ubuntu@ec2
cd /var/www/SunEdu/backend
./server_env_setup.sh
# Chọn option 2

# 4. Test
docker compose -f docker-compose.prod.yml up -d
```

### Lần deploy tiếp theo:

```bash
# Chỉ cần push code!
git push origin main

# Workflow tự động:
# - Pull code mới
# - Merge .env.production + .env.local.override
# - Deploy
```

---

✅ **Giờ .env sẽ tự động update mỗi lần deploy!**

🔒 **Passwords an toàn, chỉ tồn tại trên server!**

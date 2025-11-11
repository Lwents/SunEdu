# 🔍 File .env nào đang chạy trên EC2?

## 📊 Thứ tự ưu tiên (theo workflow)

### 1️⃣ **GitHub Secret `BACKEND_ENV_FILE`** (Ưu tiên cao nhất)
```yaml
if GitHub Secret BACKEND_ENV_FILE exists:
    .env = BACKEND_ENV_FILE secret
    ✅ Dùng file này
```

**Kiểm tra:** Vào GitHub → Settings → Secrets → Actions  
**Nếu có secret `BACKEND_ENV_FILE`** → Server dùng config này

---

### 2️⃣ **File `.env.production`** (Ưu tiên 2)
```yaml
elif .env.production exists:
    .env = .env.production
    
    if .env.local.override exists:
        .env = .env.production + .env.local.override
    ✅ Dùng file này (có thể merged)
```

**File này tự động sync từ Git**

---

### 3️⃣ **File `.env` cũ** (Ưu tiên thấp nhất)
```yaml
else:
    Keep existing .env
    ⚠️  Dùng file cũ (không tự động update)
```

---

## 🔎 CÁCH KIỂM TRA TRÊN SERVER

### Chạy script check:

```bash
# SSH vào EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Chạy script
cd /var/www/SunEdu/backend
./check_server_env.sh
```

Script sẽ show:
- ✅ File .env đang dùng
- 📋 Nội dung file
- 🔄 Nguồn gốc (Secret, .production, hay cũ)
- 💡 Khuyến nghị

---

## 📌 TÓM TẮT

### ❓ Server đang dùng file nào?

**Có 3 trường hợp:**

| Trường hợp | File đang dùng | Tự động update? |
|------------|----------------|-----------------|
| **Có GitHub Secret** | Content từ `BACKEND_ENV_FILE` secret | ✅ Khi update secret |
| **Có .env.production** | Copy từ `.env.production` (+ overrides) | ✅ Mỗi lần deploy |
| **Không có cả 2** | File `.env` cũ | ❌ Không |

---

## 🚀 KHUYẾN NGHỊ

### Để biết chính xác server đang dùng gì:

```bash
# Option 1: Chạy script check
ssh ubuntu@ec2
cd /var/www/SunEdu/backend
./check_server_env.sh

# Option 2: Check thủ công
ssh ubuntu@ec2
cat /var/www/SunEdu/backend/.env | head -20

# Option 3: Xem workflow logs
# GitHub → Actions → Deploy Backend → Xem logs
# Tìm dòng:
# "✅ Updated .env from GitHub secrets" → Dùng secret
# "📋 Using .env.production" → Dùng .production
# "⚠️ Using existing .env" → Dùng file cũ
```

---

## 💡 SETUP ĐỂ TỰ ĐỘNG UPDATE

### Hiện tại (có thể):
- ❓ Dùng GitHub secret → Phải update secret thủ công
- ❓ Dùng .env cũ → Không tự động update

### Khuyến nghị (tốt nhất):
✅ **Commit `.env.production` để tự động sync**

```bash
# 1. Đảm bảo .env.production đã đúng
cd backend
cat .env.production

# 2. Commit
git add .env.production
git commit -m "Add production config for auto-sync"
git push origin main

# 3. Setup overrides trên server (nếu cần)
ssh ubuntu@ec2
cd /var/www/SunEdu/backend
./server_env_setup.sh
# Chọn option 2 - Tạo .env.local.override

# 4. Deploy
# Từ giờ mỗi lần push → .env tự động update!
```

---

## 🆘 TROUBLESHOOTING

### Làm sao biết .env đã update sau deploy?

```bash
# Check timestamp
ssh ubuntu@ec2
stat /var/www/SunEdu/backend/.env

# Check workflow logs
# GitHub → Actions → Latest deploy → Tìm:
# "✅ Updated .env from" hoặc "✅ Created .env from"
```

### .env không update sau deploy?

**Nguyên nhân:**
1. Không có GitHub secret `BACKEND_ENV_FILE`
2. Không có file `.env.production` trong repo
3. Workflow giữ nguyên .env cũ

**Giải pháp:**
```bash
# Commit .env.production
git add backend/.env.production
git push

# Hoặc update GitHub secret
./update_github_secret.sh
```

---

✅ **Chạy `./check_server_env.sh` trên EC2 để biết chính xác!**

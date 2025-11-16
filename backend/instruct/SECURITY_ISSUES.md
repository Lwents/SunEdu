# 🚨 CÁC VẤN ĐỀ BẢO MẬT CẦN FIX TRƯỚC KHI DEPLOY

## ❌ LỖI NGHIÊM TRỌNG (CRITICAL)

### 1. DEBUG = True trong production
**Vị trí:** `backend/settings.py` line 35
**Nguy hiểm:** Lộ thông tin nhạy cảm (stack trace, queries, settings)
**Cách fix:** 
```python
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
```
✅ **ĐÃ FIX**

### 2. SECRET_KEY yếu
**Vị trí:** `docker-compose.yml`
**Hiện tại:** `dev-secret-elearing`
**Nguy hiểm:** Dễ bị đoán, session hijacking, CSRF bypass
**Cách fix:** 
```bash
./generate_secret_key.sh
# Sau đó copy vào file .env
```

### 3. Database password quá đơn giản
**Hiện tại:** `123456`
**Nguy hiểm:** Dễ bị brute force
**Cách fix:** Dùng password ít nhất 16 ký tự, có chữ hoa, số, ký tự đặc biệt
```
DB_PASSWORD=MyStr0ng!P@ssw0rd#2024
```

### 4. ALLOWED_HOSTS rỗng
**Vị trí:** `backend/settings.py`
**Nguy hiểm:** Host header attacks
**Cách fix:** Thêm domain/IP vào .env
```
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,54.xxx.xxx.xxx
```

## ⚠️ LỖI TRUNG BÌNH (HIGH)

### 5. Dùng runserver trong production
**Vị trí:** `docker-compose.yml` line 20
**Nguy hiểm:** Không ổn định, chậm, không handle concurrent requests
**Cách fix:** Dùng `docker-compose.prod.yml` đã tạo (có gunicorn)

### 6. CORS/CSRF chưa cấu hình
**Nguy hiểm:** XSS, CSRF attacks
**Cách fix:** Cấu hình trong .env
```
CSRF_TRUSTED_ORIGINS=https://your-domain.com
CORS_ALLOWED_ORIGINS=https://frontend-domain.com
```

### 7. Static files chưa được serve đúng
**Nguy hiểm:** Performance kém, không cache
**Cách fix:** Dùng nginx (xem nginx.conf.example)

## 📋 CHECKLIST TRƯỚC KHI DEPLOY

- [ ] Tạo file .env từ .env.example
- [ ] Generate SECRET_KEY mới (`./generate_secret_key.sh`)
- [ ] Đổi DB_PASSWORD mạnh
- [ ] Set DEBUG=False
- [ ] Cấu hình ALLOWED_HOSTS
- [ ] Cấu hình CSRF_TRUSTED_ORIGINS
- [ ] Cấu hình CORS_ALLOWED_ORIGINS
- [ ] Dùng docker-compose.prod.yml thay vì docker-compose.yml
- [ ] Setup nginx reverse proxy
- [ ] Cấu hình HTTPS/SSL
- [ ] Backup database trước khi deploy
- [ ] Test trên staging trước

## 🔧 FILES ĐÃ TẠO

1. ✅ `.env.example` - Template cho environment variables
2. ✅ `docker-compose.prod.yml` - Production Docker config
3. ✅ `.dockerignore` - Loại bỏ files không cần thiết
4. ✅ `.gitignore` - Ngăn commit files nhạy cảm
5. ✅ `generate_secret_key.sh` - Script tạo SECRET_KEY
6. ✅ `nginx.conf.example` - Nginx configuration
7. ✅ `DEPLOY.md` - Hướng dẫn deploy chi tiết
8. ✅ `SECURITY_ISSUES.md` - File này

## 🚀 NEXT STEPS

1. **Ngay lập tức:**
   ```bash
   # Tạo SECRET_KEY
   ./generate_secret_key.sh
   
   # Tạo file .env
   cp .env.example .env
   nano .env  # Chỉnh sửa các giá trị
   ```

2. **Khi deploy lên EC2:**
   ```bash
   # Dùng production config
   docker compose -f docker-compose.prod.yml up -d --build
   ```

3. **Sau khi deploy:**
   - Setup nginx
   - Cấu hình SSL với Let's Encrypt
   - Setup monitoring
   - Backup database định kỳ

## �� LƯU Ý

- **KHÔNG BAO GIỜ** commit file .env lên git
- **KHÔNG BAO GIỜ** expose port 5432 (PostgreSQL) ra internet
- **LUÔN LUÔN** dùng HTTPS trong production
- **THƯỜNG XUYÊN** backup database
- **THEO DÕI** logs và monitoring


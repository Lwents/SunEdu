# ⚠️ QUAN TRỌNG - ĐỌC NGAY!

## 🔴 VẤN ĐỀ: Mỗi lần deploy lại bị lỗi Bad Request (400)

### Nguyên nhân:

GitHub Actions workflow ghi đè file `.env` trên EC2 từ secret `BACKEND_ENV_FILE`.

Secret này đang **THIẾU** `api.smartedu.click` → Mỗi lần deploy lại bị lỗi!

---

## ✅ GIẢI PHÁP: Cập nhật GitHub Secret

### Bước 1: Lấy nội dung .env

```bash
# Mở file backend/.env trong editor và copy toàn bộ nội dung
# HOẶC chạy lệnh (cẩn thận, đừng share output):
cat backend/.env
```

### Bước 2: Cập nhật GitHub Secret

1. Vào: https://github.com/Lwents/SunEdu/settings/secrets/actions
2. Tìm secret `BACKEND_ENV_FILE`
3. Click **Update**
4. Paste nội dung đã copy
5. Click **Update secret**

### Bước 3: Deploy lại

```bash
git push origin develop
```

Hoặc chạy workflow thủ công trên GitHub Actions.

---

## 📚 Tài liệu chi tiết

- [UPDATE_GITHUB_SECRET.md](./UPDATE_GITHUB_SECRET.md) - Hướng dẫn chi tiết
- [copy_env_for_github.sh](./copy_env_for_github.sh) - Script copy nội dung .env

---

## 🔍 Kiểm tra sau khi deploy

```bash
# Test API
curl -I https://api.smartedu.click/admin/
# Kết quả mong đợi: HTTP/1.1 302 Found (không phải 400!)
```

---

## 📝 Lưu ý

- **KHÔNG** commit file `.env` lên git
- **LUÔN** cập nhật GitHub Secret khi thay đổi cấu hình
- **KIỂM TRA** secret trước khi deploy

---

**TÓM LẠI:** Cập nhật GitHub Secret `BACKEND_ENV_FILE` để thêm `api.smartedu.click` vào các biến:

- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `CORS_ALLOWED_ORIGINS`

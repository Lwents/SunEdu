# Tổng hợp API Endpoints - SunEdu Project

## Tổng quan
Dự án SunEdu sử dụng Django REST Framework với các module sau:
- **Backend chính**: Django REST Framework
- **Authentication**: SimpleJWT + dj-rest-auth + Google OAuth
- **Express API**: API đơn giản (port 3000)

---

## 1. Authentication & Account Management (`/api/account/`)

### 1.1 Authentication
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/account/register/` | Đăng ký tài khoản mới |
| POST | `/api/account/login/` | Đăng nhập |
| POST | `/api/account/refresh/` | Refresh JWT token |
| POST | `/api/account/logout/` | Đăng xuất |
| POST | `/api/auth/google/` | Đăng nhập Google OAuth |
| POST | `/api/auth/token/refresh/` | Refresh token (dj-rest-auth) |

### 1.2 User Profile & Password Management
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/PUT/PATCH | `/api/account/user/` | Xem/cập nhật thông tin user hiện tại |
| GET/PUT/PATCH | `/api/account/profile/` | Xem/cập nhật profile |
| POST | `/api/account/password/change/` | Đổi mật khẩu |
| POST | `/api/account/password/change/request-otp/` | Yêu cầu OTP để đổi mật khẩu |
| POST | `/api/account/password/change/confirm-otp/` | Xác nhận OTP để đổi mật khẩu |
| POST | `/api/account/password/reset/` | Yêu cầu reset mật khẩu |
| POST | `/api/account/password/reset/confirm/` | Xác nhận reset mật khẩu |
| GET | `/api/account/password/reset/confirm/<uidb64>/<token>/` | Link reset mật khẩu (legacy) |

### 1.3 Admin - User Management
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/account/admin/login/<user_id>/` | Admin đăng nhập như user |
| POST | `/api/account/admin/refresh-access/<user_id>/` | Refresh access cho user |
| POST | `/api/account/admin/logout-user/<user_id>/` | Đăng xuất user |
| GET | `/api/account/admin/users/` | Danh sách users |
| GET/PUT/PATCH/DELETE | `/api/account/admin/users/<pk>/` | Chi tiết user |
| GET | `/api/account/admin/profiles/` | Danh sách profiles |
| GET/PUT/PATCH | `/api/account/admin/profiles/<user_id>/` | Chi tiết profile |
| POST | `/api/account/admin/password/set/<user_id>/` | Set mật khẩu cho user |
| GET/POST | `/api/account/admin/maintenance/` | System maintenance |

---

## 2. AI Personalization (`/api/ai_personalization/`)

### 2.1 ViewSets (hỗ trợ CRUD đầy đủ)
| Endpoint Base | Mô tả |
|---------------|-------|
| `/api/ai_personalization/paths/` | Learning paths (CRUD) |
| `/api/ai_personalization/recommendations/` | Recommendations (CRUD) |
| `/api/ai_personalization/events/` | Learning events (CRUD) |
| `/api/ai_personalization/mastery/` | User skill mastery (CRUD) |

### 2.2 Analytics
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/ai_personalization/analytics/` | Analytics tổng hợp |
| GET | `/api/ai_personalization/skill-graph/` | Skill graph visualization |

---

## 3. Payments (`/api/payments/`)

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/payments/plans/` | Danh sách gói subscription |
| GET | `/api/payments/history/` | Lịch sử thanh toán |
| POST | `/api/payments/momo/initiate/` | Khởi tạo thanh toán MoMo |
| POST | `/api/payments/momo/ipn/` | MoMo IPN webhook |
| GET/POST | `/api/payments/momo/sync/<uuid>/` | Đồng bộ trạng thái thanh toán MoMo |

---

## 4. Content Management (`/api/content/`)

### 4.1 Subjects
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/content/subjects/` | Danh sách/tạo môn học |
| GET/PUT/PATCH/DELETE | `/api/content/subjects/<uuid>/` | Chi tiết môn học |

### 4.2 Courses
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/content/courses/` | Danh sách/tạo khóa học |
| GET/PUT/PATCH/DELETE | `/api/content/courses/<uuid>/` | Chi tiết khóa học |
| POST | `/api/content/courses/<course_id>/publish/` | Xuất bản khóa học |
| POST | `/api/content/courses/<course_id>/enroll/` | Đăng ký khóa học |

### 4.3 Modules
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/content/courses/<course_id>/modules/` | Danh sách/tạo module |
| GET/PUT/PATCH/DELETE | `/api/content/modules/<uuid>/` | Chi tiết module |
| POST | `/api/content/courses/<course_id>/modules/reorder/` | Sắp xếp lại modules |

### 4.4 Lessons
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/content/modules/<module_id>/lessons/` | Danh sách/tạo bài học |
| GET/PUT/PATCH/DELETE | `/api/content/lessons/<uuid>/` | Chi tiết bài học |
| POST | `/api/content/lessons/<lesson_id>/publish/` | Xuất bản bài học |
| GET/POST | `/api/content/lessons/<lesson_id>/progress/` | Tiến độ bài học |
| GET | `/api/content/lessons/<lesson_id>/unlock-check/` | Kiểm tra unlock bài học |

### 4.5 Lesson Versions
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/content/lessons/<lesson_id>/versions/` | Danh sách/tạo phiên bản |
| GET/PUT/PATCH/DELETE | `/api/content/lesson-versions/<uuid>/` | Chi tiết phiên bản |
| POST | `/api/content/lessons/<lesson_id>/versions/publish/` | Xuất bản phiên bản |

### 4.6 Content Blocks
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/content/lesson-versions/<version_id>/blocks/` | Danh sách/tạo content block |
| GET/PUT/PATCH/DELETE | `/api/content/content-blocks/<uuid>/` | Chi tiết content block |

### 4.7 Explorations (Interactive Content)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/content/explorations/` | Danh sách/tạo exploration |
| GET/PUT/PATCH/DELETE | `/api/content/explorations/<uuid>/` | Chi tiết exploration |
| POST | `/api/content/explorations/<exploration_id>/publish/` | Xuất bản exploration |
| GET/POST | `/api/content/explorations/<exploration_id>/states/` | States của exploration |
| GET/PUT/PATCH/DELETE | `/api/content/exploration-states/<uuid>/` | Chi tiết state |
| GET/POST | `/api/content/explorations/<exploration_id>/transitions/` | Transitions |
| GET/PUT/PATCH/DELETE | `/api/content/exploration-transitions/<uuid>/` | Chi tiết transition |

### 4.8 Content Library
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/content/content-library/` | Thư viện nội dung |
| GET/PUT/PATCH/DELETE | `/api/content/content-library/<uuid>/` | Chi tiết item |

---

## 5. Activities - Exercises & Quizzes (`/api/activities/`)

### 5.1 Exercise Management
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/activities/exercises/` | Danh sách/tạo bài tập |
| GET/PUT/PATCH/DELETE | `/api/activities/exercises/<exercise_id>/` | Chi tiết bài tập |
| POST | `/api/activities/exercises/<exercise_id>/questions/` | Thêm câu hỏi |
| DELETE | `/api/activities/questions/<question_id>/` | Xóa câu hỏi |
| POST | `/api/activities/questions/<question_id>/choices/` | Thêm đáp án |
| DELETE | `/api/activities/choices/<choice_id>/` | Xóa đáp án |

### 5.2 Student Attempt Flow
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/activities/exercises/<exercise_id>/start/` | Bắt đầu làm bài |
| POST | `/api/activities/attempts/<attempt_id>/answers/` | Nộp câu trả lời |
| POST | `/api/activities/attempts/<attempt_id>/finalize/` | Hoàn thành bài làm |
| GET | `/api/activities/attempts/<attempt_id>/` | Xem kết quả |

### 5.3 Instructor Tools
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/activities/attempts/<attempt_id>/regrade/` | Chấm lại bài |
| POST | `/api/activities/attempts/<attempt_id>/grade/` | Chấm điểm thủ công |
| GET | `/api/activities/exercises/<exercise_id>/stats/` | Thống kê bài tập |
| GET | `/api/activities/exercises/<exercise_id>/attempts/` | Danh sách bài làm |
| GET | `/api/activities/exercises/<exercise_id>/export/` | Export kết quả |

---

## 6. Admin API (`/api/admin/`)

### 6.1 Dashboard & Monitoring
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/admin/dashboard/` | Dashboard tổng quan |
| GET | `/api/admin/dashboard/active-users/` | Users online realtime |

### 6.2 User Bulk Operations
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/admin/users/bulk-create/` | Tạo users hàng loạt |
| POST | `/api/admin/users/bulk-create/rollback/` | Rollback bulk create |

### 6.3 Course Management
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/admin/courses/` | Danh sách courses |
| GET | `/api/admin/courses/<uuid>/` | Chi tiết course |
| POST | `/api/admin/courses/<uuid>/approve/` | Duyệt course |
| POST | `/api/admin/courses/<uuid>/reject/` | Từ chối course |
| POST | `/api/admin/courses/<uuid>/publish/` | Xuất bản |
| POST | `/api/admin/courses/<uuid>/unpublish/` | Hủy xuất bản |
| POST | `/api/admin/courses/<uuid>/archive/` | Lưu trữ |
| POST | `/api/admin/courses/<uuid>/restore/` | Khôi phục |
| POST | `/api/admin/courses/bulk/` | Bulk actions |

### 6.4 Transactions
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/admin/transactions/` | Danh sách giao dịch |
| GET | `/api/admin/transactions/<uuid>/` | Chi tiết giao dịch |
| GET | `/api/admin/transactions/metrics/` | Metrics |
| POST | `/api/admin/transactions/<uuid>/refund/` | Hoàn tiền |
| POST | `/api/admin/transactions/<uuid>/dispute/` | Khiếu nại |
| GET | `/api/admin/transactions/export/` | Export |

### 6.5 Reports
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/admin/reports/revenue/` | Báo cáo doanh thu |
| GET | `/api/admin/reports/users/` | Báo cáo users |
| GET | `/api/admin/reports/learning/` | Báo cáo học tập |
| GET | `/api/admin/reports/content/` | Báo cáo nội dung |

### 6.6 System Management
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/PUT | `/api/admin/system/config/` | Cấu hình hệ thống |
| GET/POST | `/api/admin/system/backups/` | Backup |
| POST | `/api/admin/system/restore/` | Restore |
| GET | `/api/admin/system/audit/` | Audit logs |
| POST | `/api/admin/system/test-email/` | Test gửi email |
| GET | `/api/admin/system/health/` | Health check |

### 6.7 Activity Logs
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/admin/activity-logs/` | Danh sách activity logs |
| GET | `/api/admin/activity-logs/<log_id>/` | Chi tiết log |

### 6.8 Security
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/PUT | `/api/admin/security/policy/` | Security policy |
| GET/POST | `/api/admin/security/ip-allowlist/` | IP whitelist |
| GET/PUT/DELETE | `/api/admin/security/ip-allowlist/<pk>/` | Chi tiết IP |
| GET | `/api/admin/security/cert/` | SSL certificate status |
| GET | `/api/admin/security/sessions/` | Active sessions |
| DELETE | `/api/admin/security/sessions/<jti>/` | Revoke session |
| GET/PUT | `/api/admin/security/alerts/` | Alert policies |

### 6.9 Notifications
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/admin/notifications/` | Danh sách thông báo |
| POST | `/api/admin/notifications/<uuid>/read/` | Đánh dấu đã đọc |
| POST | `/api/admin/notifications/read-all/` | Đọc tất cả |

---

## 7. Teacher API (`/api/teacher/`)

### 7.1 Dashboard & Students
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/teacher/dashboard/` | Dashboard giáo viên |
| GET | `/api/teacher/students/` | Danh sách học sinh |

### 7.2 Feedback
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/teacher/students/feedback/` | Gửi feedback |
| GET | `/api/teacher/students/feedback/list/` | Danh sách feedback |

### 7.3 Lesson Q&A
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/teacher/lesson-questions/` | Danh sách câu hỏi |
| POST | `/api/teacher/lesson-questions/<pk>/reply/` | Trả lời câu hỏi |
| PUT/DELETE | `/api/teacher/lesson-question-replies/<pk>/` | Sửa/xóa reply |

### 7.4 Notifications
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/teacher/notifications/` | Danh sách thông báo |
| POST | `/api/teacher/notifications/<uuid>/read/` | Đánh dấu đã đọc |
| POST | `/api/teacher/notifications/read-all/` | Đọc tất cả |

---

## 8. Student API (`/api/student/`)

### 8.1 Dashboard
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/student/dashboard/` | Dashboard học sinh |

### 8.2 Courses & Learning
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/student/courses/` | Khóa học của tôi |
| GET | `/api/student/catalog/` | Danh mục khóa học |
| GET | `/api/student/courses/<uuid>/` | Chi tiết khóa học |
| GET | `/api/student/courses/<uuid>/player/` | Course player |
| GET | `/api/student/courses/<uuid>/player/<lesson_id>/` | Player với lesson cụ thể |
| GET | `/api/student/learning-path/` | Learning path |
| POST/PUT | `/api/student/learning-path/manage/` | Quản lý learning path |

### 8.3 Lesson Q&A
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/student/lesson-questions/` | Danh sách/đặt câu hỏi |
| GET/PUT/DELETE | `/api/student/lesson-questions/<pk>/` | Chi tiết câu hỏi |
| POST | `/api/student/lesson-questions/<pk>/reply/` | Trả lời |
| POST | `/api/student/lesson-questions/<pk>/react/` | React câu hỏi |
| PUT/DELETE | `/api/student/lesson-question-replies/<reply_id>/` | Sửa/xóa reply |
| POST | `/api/student/lesson-question-replies/<reply_id>/react/` | React reply |
| POST | `/api/student/lesson-question-report/` | Báo cáo vi phạm |

### 8.4 Exams
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/student/exams/` | Danh sách kỳ thi |
| GET | `/api/student/exams/<uuid>/` | Chi tiết kỳ thi |
| POST | `/api/student/exams/<uuid>/start/` | Bắt đầu thi |
| POST | `/api/student/exams/<uuid>/submit/<attempt_id>/` | Nộp bài |
| GET | `/api/student/exams/<uuid>/result/<attempt_id>/` | Xem kết quả |
| GET | `/api/student/exams/<uuid>/ranking/` | Bảng xếp hạng |
| GET | `/api/student/exams/certificates/` | Chứng chỉ |

### 8.5 Payments
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/student/payments/history/` | Lịch sử thanh toán |
| POST | `/api/student/payments/initiate/` | Khởi tạo thanh toán |

### 8.6 Account
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/PUT | `/api/student/account/profile/` | Profile |
| POST | `/api/student/account/change-password/` | Đổi mật khẩu |
| GET | `/api/student/account/parent/` | Thông tin phụ huynh |

### 8.7 Notifications
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/student/notifications/` | Danh sách thông báo |
| POST | `/api/student/notifications/<uuid>/read/` | Đánh dấu đã đọc |
| POST | `/api/student/notifications/read-all/` | Đọc tất cả |

---

## 9. School Management (chưa include trong main URLs)

### 9.1 Schools
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/schools/` | Danh sách/tạo trường |
| GET/PUT/PATCH/DELETE | `/schools/<uuid>/` | Chi tiết trường |

### 9.2 Classrooms
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/schools/<school_id>/classrooms/` | Danh sách/tạo lớp |
| GET/PUT/PATCH/DELETE | `/classrooms/<uuid>/` | Chi tiết lớp |

### 9.3 Memberships
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/classrooms/<classroom_id>/members/` | Danh sách/thêm member |
| GET/PUT/DELETE | `/classrooms/<classroom_id>/members/<user_id>/` | Chi tiết member |

### 9.4 Enrollments
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/classrooms/<classroom_id>/enrollments/` | Danh sách/tạo enrollment |
| GET/PUT/DELETE | `/enrollments/<uuid>/` | Chi tiết enrollment |

### 9.5 Invitations
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/classrooms/<classroom_id>/invitations/` | Danh sách/tạo lời mời |
| POST | `/invitations/<uuid>/accept/` | Chấp nhận lời mời |
| POST | `/invitations/<uuid>/revoke/` | Thu hồi lời mời |

---

## 10. Media & Static Files

| Endpoint | Mô tả |
|----------|-------|
| GET | `/api/media/stream/<path>` | Stream media files (hỗ trợ HTTP Range) |
| GET | `/media/<path>` | Serve media files (development) |

---

## 11. Express API (Port 3000)

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Test endpoint |

---

## Ghi chú

### Module tạm thời bị tắt:
- ❌ `/api/assignments/` - Assignments module (import errors)

### Authentication Methods:
1. **JWT Token**: Bearer token trong header `Authorization: Bearer <token>`
2. **Google OAuth**: POST đến `/api/auth/google/`
3. **Session**: Django session-based auth cho admin

### Permissions:
- **IsAuthenticated**: Yêu cầu đăng nhập
- **IsAdminUser**: Chỉ admin
- **IsTeacher**: Chỉ giáo viên
- **IsStudent**: Chỉ học sinh
- **IsOwner**: Chỉ owner của resource

### Response Format:
Hầu hết API trả về JSON format:
```json
{
  "status": "success",
  "data": {...},
  "message": "Optional message"
}
```

### Pagination:
APIs sử dụng pagination với params:
- `page`: Số trang
- `page_size`: Số items/trang
- `limit`/`offset`: Alternative pagination

### Filtering & Search:
Nhiều list endpoints hỗ trợ:
- `search`: Full-text search
- `ordering`: Sắp xếp (-field_name cho DESC)
- Các filters cụ thể theo từng endpoint

---

**Tổng số endpoints**: ~200+ API endpoints
**Base URL Production**: https://api.sunedu.vn (giả định)
**Base URL Development**: http://localhost:8000

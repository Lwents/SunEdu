# Student API Test Guide

## Đã sửa các lỗi:

1. **ExerciseSettings không có field 'grade'**: 
   - Đã xóa việc truy cập `exercise.settings.grade` 
   - Sử dụng giá trị mặc định 'Khối 1–2' cho grade

2. **Import errors**: 
   - Tất cả imports đã được kiểm tra và đúng
   - Các view classes đã được export đúng trong `__init__.py`

3. **Permission handling**: 
   - Đã thêm `IsStudent` permission cho tất cả endpoints
   - Đảm bảo chỉ student users mới có thể truy cập

## Cách test:

### 1. Test với Django shell (nếu có Django environment):

```bash
cd /home/lwent/Documents/SunEdu/backend
python manage.py shell
```

Trong shell:
```python
from student_api.views import StudentDashboardView
from student_api.permissions import IsStudent
print("✓ Imports successful")
```

### 2. Test với server chạy:

```bash
# Start server
python manage.py runserver

# Test endpoints với curl (cần JWT token)
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/student/dashboard/
```

### 3. Test với script:

```bash
# Test imports (cần Django environment)
python3 test_student_imports.py

# Test endpoints (cần server chạy và JWT token)
python3 test_student_endpoints.py <jwt_token>
```

## Các endpoints đã triển khai:

### Dashboard
- `GET /api/student/dashboard/` - Dashboard với resume course, featured courses, preview exams

### Courses
- `GET /api/student/courses/` - My Courses (enrolled courses với progress)
- `GET /api/student/catalog/` - Course Catalog (tất cả published courses)
- `GET /api/student/courses/<uuid:pk>/` - Course Detail
- `GET /api/student/courses/<uuid:pk>/player/` - Course Player (lesson content)
- `GET /api/student/courses/<uuid:pk>/player/<uuid:lesson_id>/` - Course Player với lesson cụ thể
- `GET /api/student/learning-path/` - Learning Path

### Exams
- `GET /api/student/exams/` - Exams List
- `GET /api/student/exams/<uuid:pk>/` - Exam Detail
- `POST /api/student/exams/<uuid:pk>/start/` - Start Exam
- `POST /api/student/exams/<uuid:pk>/submit/<uuid:attempt_id>/` - Submit Exam
- `GET /api/student/exams/<uuid:pk>/result/<uuid:attempt_id>/` - Exam Result
- `GET /api/student/exams/<uuid:pk>/ranking/` - Exam Ranking
- `GET /api/student/exams/certificates/` - Certificates

### Payments
- `GET /api/student/payments/history/` - Payment History
- `POST /api/student/payments/initiate/` - Initiate Payment

### Account
- `GET /api/student/account/profile/` - Get Profile
- `PUT /api/student/account/profile/` - Update Profile
- `POST /api/student/account/change-password/` - Change Password
- `GET /api/student/account/parent/` - Get Parent Info
- `PUT /api/student/account/parent/` - Update Parent Info

## Lưu ý:

1. Tất cả endpoints yêu cầu authentication (JWT token)
2. Chỉ student users mới có thể truy cập (IsStudent permission)
3. Một số endpoints cần course/exam IDs hợp lệ để test đầy đủ
4. Exercise model không có field 'grade', nên grade được set mặc định là 'Khối 1–2'

## Nếu gặp lỗi:

1. Kiểm tra Django environment đã được activate chưa
2. Kiểm tra database migrations đã chạy chưa: `python manage.py migrate`
3. Kiểm tra JWT token có hợp lệ không
4. Kiểm tra user có role='student' và is_staff=False



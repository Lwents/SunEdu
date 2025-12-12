// src/router/index.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

// Layouts - Lazy load để giảm bundle size
const AdminLayout = () => import('@/layouts/AdminLayout.vue')
const TeacherLayout = () => import('@/layouts/TeacherLayout.vue')
const StudentLayout = () => import('@/layouts/StudentLayout.vue')
const AuthLayout = () => import('@/layouts/AuthLayout.vue')

// Pinia store (dùng trong guard)
import { useAuthStore } from '@/store/auth.store'

const routes: RouteRecordRaw[] = [
  // Landing
  {
    path: '/',
    component: () => import('@/pages/common/Landing.vue'),
    meta: { title: 'Trang chủ' },
  },

  // Auth
  {
    path: '/auth',
    component: AuthLayout,
    children: [
      { path: '', redirect: '/auth/login' },
      {
        path: 'login',
        component: () => import('@/pages/auth/Login.vue'),
        meta: {
          title: 'Đăng nhập 🎓',
          desc: 'Nhập thông tin để vào lớp học nhé!',
        },
      },
      {
        path: 'register',
        component: () => import('@/pages/auth/Register.vue'),
        meta: {
          title: 'Đăng ký ✨',
          desc: 'Tạo tài khoản mới để bắt đầu hành trình học tập!',
        },
      },
      {
        path: 'forgot-password',
        component: () => import('@/pages/auth/ForgotPassword.vue'),
        meta: { title: 'Quên mật khẩu' },
      },
      {
        path: 'reset-password',
        component: () => import('@/pages/auth/ResetPassword.vue'),
        meta: { title: 'Đặt lại mật khẩu', hideSimpleHeader: true },
      },
    ],
  },

  // Admin
  {
    path: '/admin',
    component: AdminLayout,
    meta: { role: 'admin' },
    children: [
      { path: '', redirect: '/admin/dashboard' },

      {
        path: 'dashboard',
        component: () => import('@/pages/admin/dashboard/Dashboard.vue'),
        meta: { title: 'Trang chủ' },
      },

      // Users
      {
        path: 'users',
        component: () => import('@/pages/admin/users/Users.vue'),
        meta: { title: 'Quản lý người dùng' },
      },
      {
        path: 'users/bulk-create',
        component: () => import('@/pages/admin/users/BulkCreate.vue'),
        meta: { title: 'Tạo tài khoản hàng loạt' },
      },
      {
        path: 'users/:id',
        component: () => import('@/pages/admin/users/UserDetail.vue'),
        // meta: { title: (to: any) => `Người dùng #${to.params.id}` },
        meta: { title: `Hồ sơ người dùng` },
      },

      // Courses
      {
        path: 'courses',
        component: () => import('@/pages/admin/courses/Courses.vue'),
        meta: { title: 'Quản lý khóa học' },
      },
      {
        path: 'courses/approval',
        component: () => import('@/pages/admin/courses/CourseApproval.vue'),
        meta: { title: 'Duyệt khóa học' },
      },
      {
        path: 'courses/:id',
        component: () => import('@/pages/admin/courses/CourseDetail.vue'),
        meta: { title: (to: any) => `Chi tiết khóa học #${to.params.id}` },
      },

      // System - Order matters: specific routes first, then general
      {
        path: 'system/activity',
        component: () => import('@/pages/admin/system/ActivityLogs.vue'),
        meta: { title: 'Log hoạt động' },
      },
      {
        path: 'system/security',
        component: () => import('@/pages/admin/system/SecuritySettings.vue'),
        meta: { title: 'Bảo mật hệ thống' },
      },
      {
        path: 'system',
        component: () => import('@/pages/admin/system/SystemConfig.vue'),
        meta: { title: 'Cấu hình hệ thống' },
      },

      // Reports
      {
        path: 'reports/revenue',
        component: () => import('@/pages/admin/reports/RevenueReports.vue'),
        meta: { title: 'Báo cáo doanh thu' },
      },
      {
        path: 'reports/users',
        component: () => import('@/pages/admin/reports/UserAnalytics.vue'),
        meta: { title: 'Phân tích người dùng' },
      },
      {
        path: 'reports/learning',
        component: () => import('@/pages/admin/reports/LearningAnalytics.vue'),
        meta: { title: 'Phân tích học tập' },
      },
      {
        path: 'reports/content',
        component: () => import('@/pages/admin/reports/ContentAnalytics.vue'),
        meta: { title: 'Phân tích nội dung' },
      },
      {
        path: 'reports/export',
        component: () => import('@/pages/admin/reports/ReportsExport.vue'),
        meta: { title: 'Xuất báo cáo' },
      },

      // Transactions
      {
        path: 'transactions',
        component: () => import('@/pages/admin/transactions/Transactions.vue'),
        meta: { title: 'Giao dịch' },
      },
      {
        path: 'transactions/:id',
        component: () => import('@/pages/admin/transactions/TransactionDetail.vue'),
        meta: { title: (to: any) => `Chi tiết giao dịch #${to.params.id}` },
      },
    ],
  },

  // Teacher
  {
    path: '/teacher',
    component: TeacherLayout,
    meta: { role: 'instructor' },
    children: [
      { path: '', redirect: '/teacher/dashboard' },
      {
        path: 'dashboard',
        component: () => import('@/pages/teacher/dashboard/dashboard.vue'),
        meta: { title: 'Trang chủ giảng viên' },
      },
      {
        path: 'lesson-qa',
        name: 'teacher-lesson-qa',
        component: () => import('@/pages/teacher/courses/LessonQA.vue'),
        meta: { title: 'Hỏi đáp bài học' },
      },

      //account
      {
        path: 'account/profile',
        name: 'teacher-account-profile',
        component: () => import('@/pages/teacher/account/Profile.vue'),
        meta: { title: 'Tài khoản giáo viên' },
      },
      {
        path: 'account/change-password',
        name: 'teacher-account-change-password',
        component: () => import('@/pages/teacher/account/ChanePassword.vue'),
        meta: { title: 'Đổi mật khẩu' },
      },
      // courses
      {
        path: 'courses',
        name: 'teacher-courses',
        component: () => import('@/pages/teacher/courses/Courses.vue'),
        meta: { title: 'Khoá học của tôi' },
      },
      {
        path: 'courses/new',
        name: 'teacher-course-new',
        component: () => import('@/pages/teacher/courses/CourseCreateWizard.vue'),
        meta: { title: 'Tạo khoá học' },
      },
      {
        path: 'courses/:id',
        name: 'teacher-course-detail',
        component: () => import('@/pages/teacher/courses/CourseDetail.vue'),
        meta: { title: (to: any) => `Khoá học #${to.params.id}` },
      },
      {
        path: 'courses/:id/edit',
        name: 'teacher-course-edit',
        component: () => import('@/pages/teacher/courses/CourseEdit.vue'),
        meta: { title: (to: any) => `Sửa khoá học #${to.params.id}` },
      },
      {
        path: 'courses/content-library',
        name: 'teacher-content-library',
        component: () => import('@/pages/teacher/courses/ContentLibrary.vue'),
        meta: { title: 'Thư viện nội dung' },
      },

      // class
      {
        path: 'classes',
        component: () => import('@/pages/teacher/classes/Classes.vue'),
        meta: { title: 'Lớp học' },
      },
      {
        path: 'classes/:id',
        name: 'teacher-class-detail',
        component: () => import('@/pages/teacher/classes/ClassDetail.vue'),
        meta: { title: (to: any) => `Lớp #${to.params.id}` },
      },
      {
        path: 'classes/:id/assignments',
        name: 'teacher-class-assign',
        component: () => import('@/pages/teacher/classes/Assignments.vue'),
        meta: { title: 'Giao bài tập' },
      },
      {
        path: 'classes/:id/live',
        name: 'teacher-class-live',
        component: () => import('@/pages/teacher/classes/OnlineClass.vue'),
        meta: { title: 'Lớp trực tuyến' },
      },

      // exams
      {
        path: 'exams',
        component: () => import('@/pages/teacher/exams/Exams.vue'),
        meta: { title: 'Bài kiểm tra' },
      },
      {
        path: 'exams/new',
        name: 'teacher-exam-new',
        component: () => import('@/pages/teacher/exams/ExamCreate.vue'),
        meta: { title: 'Tạo bài kiểm tra' },
      },
      {
        path: 'exams/:id',
        name: 'teacher-exam-detail',
        component: () => import('@/pages/teacher/exams/ExamDetail.vue'),
        meta: { title: (to: any) => `Đề #${to.params.id}` },
      },
      {
        path: 'exams/:id/edit',
        name: 'teacher-exam-edit',
        component: () => import('@/pages/teacher/exams/ExamEdit.vue'),
        meta: { title: (to: any) => `Sửa đề #${to.params.id}` },
      },
      {
        path: 'exams/:id/grading',
        name: 'teacher-exam-grading',
        component: () => import('@/pages/teacher/exams/ExamGrading.vue'),
        meta: { title: 'Chấm bài' },
      },
      {
        path: 'reports',
        name: 'teacher-reports',
        component: () => import('@/pages/teacher/exams/ExamReports.vue'),
        meta: { title: 'Báo cáo chấm thi' },
      },

      // games
      {
        path: 'games',
        name: 'teacher-games',
        component: () => import('@/pages/teacher/games/GamesList.vue'),
        meta: { title: 'Quản lý trò chơi' },
      },

      //students feedback
      {
        path: 'students',
        name: 'teacher-students',
        component: () => import('@/pages/teacher/students/Students.vue'),
        meta: { title: 'Học viên của tôi' },
      },
      {
        path: 'students/progress',
        name: 'teacher-students-progress',
        component: () => import('@/pages/teacher/students/StudentProgress.vue'),
        meta: { title: 'Tiến độ học viên' },
      },
      {
        path: 'students/feedback',
        name: 'teacher-students-feedback',
        component: () => import('@/pages/teacher/students/Feedback.vue'),
        meta: { title: 'Phản hồi học viên' },
      },
      // Course Content Management
      {
        path: 'courses/:id/content',
        name: 'teacher-course-content',
        component: () => import('@/pages/teacher/courses/CourseContent.vue'),
        props: true,
        meta: { title: 'Quản lý nội dung khóa học' },
      },
      {
        path: 'lessons/:id/edit',
        name: 'teacher-lesson-edit',
        component: () => import('@/pages/teacher/courses/LessonEdit.vue'),
        props: true,
        meta: { title: 'Chỉnh sửa bài học' },
      },
    ],
  },

  // Student
  {
    path: '/student',
    component: StudentLayout,
    meta: { role: 'student' },
    children: [
      { path: '', redirect: '/student/dashboard' },
      {
        path: 'dashboard',
        name: 'student-dashboard',
        component: () => import('@/pages/student/dashboard/dashboard.vue'),
        meta: { title: 'Trang chủ' },
      },

      // MyCourses
      {
        path: 'courses',
        name: 'MyCourses',
        component: () => import('@/pages/student/courses/MyCourses.vue'),
        meta: { title: 'Khoá học của tôi' },
      },

      // Catalog / Detail / Player / Learning Path
      {
        path: 'catalog',
        name: 'student-catalog',
        component: () => import('@/pages/student/courses/Catalog.vue'),
        meta: { title: 'Danh mục khoá học' },
      },
      {
        path: 'courses/:id',
        name: 'student-course-detail',
        component: () => import('@/pages/student/courses/CourseDetail.vue'),
        props: true,
        meta: { title: (to: any) => `Khoá học #${to.params.id}` },
      },
      {
        path: 'courses/:id/player/:lessonId?',
        name: 'student-course-player',
        component: () => import('@/pages/student/courses/CoursePlayer.vue'),
        props: true,
        meta: { title: (to: any) => `Bài học #${to.params.lessonId ?? ''}` },
      },
      {
        path: 'learning-path',
        name: 'student-learning-path',
        component: () => import('@/pages/student/courses/LearningPath.vue'),
        meta: { title: 'Lộ trình học' },
      },

      // Exams
      {
        path: 'exams',
        name: 'student-exams',
        component: () => import('@/pages/student/exams/PracticeExams.vue'),
        meta: { title: 'Luyện đề' },
      },
      // Đặt result route TRƯỚC detail route để match chính xác
      {
        path: 'exams/:id/result',
        name: 'student-exam-result',
        component: () => import('@/pages/student/exams/ExamResult.vue'),
        props: true,
        meta: { title: 'Kết quả bài thi' },
      },
      {
        path: 'exams/:id',
        name: 'student-exam-detail',
        component: () => import('@/pages/student/exams/ExamDetail.vue'),
        props: true,
        meta: { title: (to: any) => `Đề #${to.params.id}` },
      },
      {
        path: 'exams/certificates',
        name: 'student-certificates',
        component: () => import('@/pages/student/exams/Certificates.vue'),
        meta: { title: 'Chứng chỉ' },
      },
      {
        path: 'exams/ranking',
        name: 'student-exams-ranking',
        component: () => import('@/pages/student/exams/Ranking.vue'),
        meta: { title: 'Bảng xếp hạng' },
      },

      // Games
      {
        path: 'games',
        name: 'student-games',
        component: () => import('@/pages/student/games/Games.vue'),
        meta: { title: 'Trò chơi' },
      },

      // Payments & Account
      {
        path: 'payments',
        name: 'student-payments',
        component: () => import('@/pages/student/payments/Payments.vue'),
        meta: { title: 'Nạp tiền' },
      },
      {
        path: 'payments/history',
        name: 'student-payments-history',
        component: () => import('@/pages/student/payments/History.vue'),
        meta: { title: 'Lịch sử nạp tiền' },
      },
      {
        path: 'account/profile',
        name: 'student-profile',
        component: () => import('@/pages/student/account/Profile.vue'),
        meta: { title: 'Hồ sơ cá nhân' },
      },
      {
        path: 'account/change-password',
        name: 'student-change-password',
        component: () => import('@/pages/student/account/ChangePassword.vue'),
        meta: { title: 'Đổi mật khẩu' },
      },
      {
        path: 'account/parent',
        name: 'student-parent',
        component: () => import('@/pages/student/account/ParentView.vue'),
        meta: { title: 'Thông tin phụ huynh' },
      },
      {
        path: 'payments/cart',
        name: 'student-payments-cart',
        component: () => import('@/pages/student/payments/Cart.vue'),
        meta: { title: 'Giỏ hàng' },
      },
      {
        path: 'payments/checkout',
        name: 'student-payments-checkout',
        component: () => import('@/pages/student/payments/Checkout.vue'),
        meta: { title: 'Nạp tiền' },
      },
    ],
  },

  // Common
  {
    path: '/notifications',
    component: () => import('@/pages/common/Notifications.vue'),
    meta: { title: 'Thông báo' },
  },
  {
    path: '/:pathMatch(.*)*',
    component: () => import('@/pages/common/NotFound.vue'),
    meta: { title: 'Không tìm thấy trang' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Guard đơn giản theo role + tự hydrate từ localStorage
router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()
  // Hydrate từ storage nếu chưa có user nhưng có token
  if (!auth.user && (auth.token || localStorage.getItem('accessToken'))) {
    auth.hydrateFromStorage()
  }

  // Kiểm tra cả token và user để đảm bảo đã đăng nhập
  const isAuthenticated = auth.isAuthenticated && auth.user && auth.token

  // Đã đăng nhập mà vào /auth → đẩy về khu đúng role
  if (to.path.startsWith('/auth') && isAuthenticated) {
    auth.redirectByRole(auth.user!.role)
    return
  }

  // Chưa đăng nhập mà vào khu riêng → đẩy về login
  const needRole = to.meta.role as 'admin' | 'instructor' | 'student' | undefined
  if (needRole && !isAuthenticated) {
    next('/auth/login')
    return
  }

  // Sai role → đẩy về khu đúng
  if (needRole && isAuthenticated && auth.user && auth.user.role !== needRole) {
    auth.redirectByRole(auth.user.role)
    return
  }

  // Nếu đang ở "/" mà đã login → về dashboard theo role
  if (to.path === '/' && isAuthenticated && auth.user) {
    auth.redirectByRole(auth.user.role)
    return
  }

  next()
})
router.afterEach((to) => {
  // tìm route con có meta.title gần nhất
  const r = [...to.matched].reverse().find((r) => (r.meta as any)?.title !== undefined)
  if (!r) return
  const raw = (r.meta as any).title
  const title = typeof raw === 'function' ? raw(to) : raw
  if (title) document.title = String(title)
})
export default router

from django.urls import path
from student_api.views import (
    StudentDashboardView,
    StudentMyCoursesView,
    StudentCourseCatalogView,
    StudentCourseDetailView,
    StudentCoursePlayerView,
    StudentLearningPathView,
    StudentExamsListView,
    StudentExamDetailView,
    StudentExamStartView,
    StudentExamSubmitView,
    StudentExamResultView,
    StudentExamRankingView,
    StudentCertificatesView,
    StudentPaymentsHistoryView,
    StudentPaymentsInitiateView,
    StudentProfileView,
    StudentChangePasswordView,
    StudentParentViewView,
)
from student_api.views.notifications_view import (
    StudentNotificationsView,
    StudentNotificationReadView,
    StudentNotificationReadAllView,
)

app_name = 'student_api'

urlpatterns = [
    # Dashboard
    path('dashboard/', StudentDashboardView.as_view(), name='dashboard'),
    
    # Courses
    path('courses/', StudentMyCoursesView.as_view(), name='my-courses'),
    path('catalog/', StudentCourseCatalogView.as_view(), name='catalog'),
    path('courses/<uuid:pk>/', StudentCourseDetailView.as_view(), name='course-detail'),
    path('courses/<uuid:pk>/player/', StudentCoursePlayerView.as_view(), name='course-player'),
    path('courses/<uuid:pk>/player/<uuid:lesson_id>/', StudentCoursePlayerView.as_view(), name='course-player-lesson'),
    path('learning-path/', StudentLearningPathView.as_view(), name='learning-path'),
    
    # Exams
    path('exams/', StudentExamsListView.as_view(), name='exams-list'),
    path('exams/<uuid:pk>/', StudentExamDetailView.as_view(), name='exam-detail'),
    path('exams/<uuid:pk>/start/', StudentExamStartView.as_view(), name='exam-start'),
    path('exams/<uuid:pk>/submit/<uuid:attempt_id>/', StudentExamSubmitView.as_view(), name='exam-submit'),
    path('exams/<uuid:pk>/result/<uuid:attempt_id>/', StudentExamResultView.as_view(), name='exam-result'),
    path('exams/<uuid:pk>/ranking/', StudentExamRankingView.as_view(), name='exam-ranking'),
    path('exams/certificates/', StudentCertificatesView.as_view(), name='certificates'),
    
    # Payments
    path('payments/history/', StudentPaymentsHistoryView.as_view(), name='payments-history'),
    path('payments/initiate/', StudentPaymentsInitiateView.as_view(), name='payments-initiate'),
    
    # Account
    path('account/profile/', StudentProfileView.as_view(), name='profile'),
    path('account/change-password/', StudentChangePasswordView.as_view(), name='change-password'),
    path('account/parent/', StudentParentViewView.as_view(), name='parent'),
    
    # Notifications
    path('notifications/', StudentNotificationsView.as_view(), name='notifications'),
    path('notifications/<uuid:id>/read/', StudentNotificationReadView.as_view(), name='notification-read'),
    path('notifications/read-all/', StudentNotificationReadAllView.as_view(), name='notification-read-all'),
]



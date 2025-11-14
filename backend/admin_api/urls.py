from django.urls import path
from admin_api.views import (
    AdminDashboardView,
    AdminCourseListView, AdminCourseDetailView,
    AdminCourseApproveView, AdminCourseRejectView,
    AdminCoursePublishView, AdminCourseUnpublishView,
    AdminCourseArchiveView, AdminCourseRestoreView,
    AdminCourseBulkActionView,
    AdminTransactionListView, AdminTransactionDetailView,
    AdminTransactionMetricsView, AdminTransactionRefundView,
    AdminTransactionDisputeView, AdminTransactionExportView,
    AdminRevenueReportView, AdminUserReportView,
    AdminLearningReportView, AdminContentReportView,
    AdminSystemConfigView, AdminSystemBackupView,
    AdminSystemRestoreView, AdminSystemAuditView,
    AdminSystemTestEmailView,
    AdminActivityLogView,
    AdminSecurityPolicyView,
    AdminIpAllowListView,
    AdminIpAllowDetailView,
    AdminCertStatusView,
    AdminSessionListView,
    AdminSessionRevokeView,
    AdminAlertPolicyView
)

app_name = 'admin_api'

urlpatterns = [
    # Dashboard
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),

    # Courses
    path('courses/', AdminCourseListView.as_view(), name='course-list'),
    path('courses/<uuid:pk>/', AdminCourseDetailView.as_view(), name='course-detail'),
    path('courses/<uuid:pk>/approve/', AdminCourseApproveView.as_view(), name='course-approve'),
    path('courses/<uuid:pk>/reject/', AdminCourseRejectView.as_view(), name='course-reject'),
    path('courses/<uuid:pk>/publish/', AdminCoursePublishView.as_view(), name='course-publish'),
    path('courses/<uuid:pk>/unpublish/', AdminCourseUnpublishView.as_view(), name='course-unpublish'),
    path('courses/<uuid:pk>/archive/', AdminCourseArchiveView.as_view(), name='course-archive'),
    path('courses/<uuid:pk>/restore/', AdminCourseRestoreView.as_view(), name='course-restore'),
    path('courses/bulk/', AdminCourseBulkActionView.as_view(), name='course-bulk'),

    # Transactions
    path('transactions/', AdminTransactionListView.as_view(), name='transaction-list'),
    path('transactions/<uuid:pk>/', AdminTransactionDetailView.as_view(), name='transaction-detail'),
    path('transactions/metrics/', AdminTransactionMetricsView.as_view(), name='transaction-metrics'),
    path('transactions/<uuid:pk>/refund/', AdminTransactionRefundView.as_view(), name='transaction-refund'),
    path('transactions/<uuid:pk>/dispute/', AdminTransactionDisputeView.as_view(), name='transaction-dispute'),
    path('transactions/export/', AdminTransactionExportView.as_view(), name='transaction-export'),

    # Reports
    path('reports/revenue/', AdminRevenueReportView.as_view(), name='report-revenue'),
    path('reports/users/', AdminUserReportView.as_view(), name='report-users'),
    path('reports/learning/', AdminLearningReportView.as_view(), name='report-learning'),
    path('reports/content/', AdminContentReportView.as_view(), name='report-content'),

    # System
    path('system/config/', AdminSystemConfigView.as_view(), name='system-config'),
    path('system/backups/', AdminSystemBackupView.as_view(), name='system-backups'),
    path('system/restore/', AdminSystemRestoreView.as_view(), name='system-restore'),
    path('system/audit/', AdminSystemAuditView.as_view(), name='system-audit'),
    path('system/test-email/', AdminSystemTestEmailView.as_view(), name='system-test-email'),

    # Activity Logs
    path('activity-logs/', AdminActivityLogView.as_view(), name='activity-logs'),

    # Security
    path('security/policy/', AdminSecurityPolicyView.as_view(), name='security-policy'),
    path('security/ip-allowlist/', AdminIpAllowListView.as_view(), name='security-ip-allowlist'),
    path('security/ip-allowlist/<str:pk>/', AdminIpAllowDetailView.as_view(), name='security-ip-allowlist-detail'),
    path('security/cert/', AdminCertStatusView.as_view(), name='security-cert'),
    path('security/sessions/', AdminSessionListView.as_view(), name='security-sessions'),
    path('security/sessions/<str:jti>/', AdminSessionRevokeView.as_view(), name='security-session-revoke'),
    path('security/alerts/', AdminAlertPolicyView.as_view(), name='security-alerts'),
]



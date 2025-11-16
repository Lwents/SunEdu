from .dashboard_view import StudentDashboardView
from .courses_view import (
    StudentMyCoursesView,
    StudentCourseCatalogView,
    StudentCourseDetailView,
    StudentCoursePlayerView,
    StudentLearningPathView,
)
from .exams_view import (
    StudentExamsListView,
    StudentExamDetailView,
    StudentExamStartView,
    StudentExamSubmitView,
    StudentExamResultView,
    StudentExamRankingView,
    StudentCertificatesView,
)
from .payments_view import (
    StudentPaymentsHistoryView,
    StudentPaymentsInitiateView,
)
from .account_view import (
    StudentProfileView,
    StudentChangePasswordView,
    StudentParentViewView,
)

__all__ = [
    'StudentDashboardView',
    'StudentMyCoursesView',
    'StudentCourseCatalogView',
    'StudentCourseDetailView',
    'StudentCoursePlayerView',
    'StudentLearningPathView',
    'StudentExamsListView',
    'StudentExamDetailView',
    'StudentExamStartView',
    'StudentExamSubmitView',
    'StudentExamResultView',
    'StudentExamRankingView',
    'StudentCertificatesView',
    'StudentPaymentsHistoryView',
    'StudentPaymentsInitiateView',
    'StudentProfileView',
    'StudentChangePasswordView',
    'StudentParentViewView',
]



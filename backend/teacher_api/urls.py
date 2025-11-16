from django.urls import path
from teacher_api.views import TeacherDashboardView, TeacherStudentsView
from teacher_api.views.feedback_view import TeacherFeedbackView, TeacherFeedbackListView

app_name = 'teacher_api'

urlpatterns = [
    path('dashboard/', TeacherDashboardView.as_view(), name='dashboard'),
    path('students/', TeacherStudentsView.as_view(), name='students'),
    path('students/feedback/', TeacherFeedbackView.as_view(), name='feedback'),
    path('students/feedback/list/', TeacherFeedbackListView.as_view(), name='feedback-list'),
]








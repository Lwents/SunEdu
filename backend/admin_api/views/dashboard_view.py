from datetime import datetime, timedelta
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from admin_api.permissions import IsAdmin
from custom_account.models import UserModel
from content.models import Course
from payments.models import Payment


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Get dashboard KPIs and stats"""
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        # DAU (Daily Active Users) - users who logged in today
        dau = UserModel.objects.filter(
            last_login__gte=today_start
        ).count()

        # New signups in last 7 days
        signups7d = UserModel.objects.filter(
            created_on__gte=week_ago
        ).count()

        # GMV today (Gross Merchandise Value)
        payments_today = Payment.objects.filter(
            created_at__gte=today_start,
            status='paid'
        )
        gmv_today = payments_today.aggregate(total=Sum('amount'))['total'] or 0

        # Transactions today
        tx_today = payments_today.count()

        # Refund rate (7 days)
        payments_7d = Payment.objects.filter(created_at__gte=week_ago)
        total_7d = payments_7d.aggregate(total=Sum('amount'))['total'] or 0
        refunds_7d = payments_7d.filter(status='refunded').aggregate(total=Sum('amount'))['total'] or 0
        refund_rate_7d = (refunds_7d / total_7d * 100) if total_7d > 0 else 0

        # Pending approvals (courses pending review)
        approvals_pending = Course.objects.filter(
            published=False
        ).count()

        # Top courses by enrollments (mock - need enrollment model)
        top_courses = Course.objects.filter(
            published=True
        ).annotate(
            enrollments_count=Count('id')  # Placeholder - need actual enrollment count
        ).order_by('-enrollments_count')[:5]

        top_courses_data = [
            {
                'id': str(course.id),
                'title': course.title,
                'enrollments': getattr(course, 'enrollments_count', 0)
            }
            for course in top_courses
        ]

        # Recent transactions
        recent_transactions = Payment.objects.filter(
            created_at__gte=month_ago
        ).select_related('user', 'plan').order_by('-created_at')[:10]

        recent_tx_data = [
            {
                'id': str(tx.id),
                'user': tx.user.email if tx.user else 'N/A',
                'course': tx.plan.name if tx.plan else 'N/A',
                'amount': float(tx.amount),
                'gateway': tx.metadata.get('gateway', 'N/A') if tx.metadata else 'N/A',
                'status': tx.status
            }
            for tx in recent_transactions
        ]

        # Pending approvals
        pending_approvals = Course.objects.filter(
            published=False
        ).select_related('owner').order_by('-id')[:10]

        pending_approvals_data = [
            {
                'id': str(course.id),
                'title': course.title,
                'teacher': course.owner.email if course.owner else 'N/A',
                'submittedAt': course.id.hex[:8]  # Placeholder for submitted date
            }
            for course in pending_approvals
        ]

        # Security stats (mock - need actual security model)
        security = {
            'failedLogins24h': 0,  # Placeholder
            'lockedAccounts': 0,  # Placeholder
            'sslDaysToExpire': 30  # Placeholder
        }

        # System health (mock - need actual monitoring)
        system = {
            'cpuP95': 45,  # Placeholder
            'ramP95': 62,  # Placeholder
            'disk': 78,  # Placeholder
            'backup': {
                'lastRun': '2024-01-01 00:00:00',  # Placeholder
                'status': 'success'  # Placeholder
            }
        }

        return Response({
            'kpis': {
                'dau': dau,
                'signups7d': signups7d,
                'gmvToday': float(gmv_today),
                'txToday': tx_today,
                'refundRate7d': round(refund_rate_7d, 2),
                'approvalsPending': approvals_pending
            },
            'topCourses': top_courses_data,
            'recentTransactions': recent_tx_data,
            'pendingApprovals': pending_approvals_data,
            'security': security,
            'system': system
        }, status=status.HTTP_200_OK)



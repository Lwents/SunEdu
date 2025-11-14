from datetime import datetime, timedelta
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from django.http import HttpResponse
import csv
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from admin_api.permissions import IsAdmin
from payments.models import Payment
from content.models import Course
from custom_account.models import UserModel


class AdminRevenueReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Get revenue reports"""
        report_type = request.query_params.get('type', 'timeseries')  # timeseries, by-gateway, top-courses
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        granularity = request.query_params.get('granularity', 'day')  # day, week, month

        if not from_date:
            from_date = (timezone.now() - timedelta(days=30)).date()
        else:
            from_date = datetime.fromisoformat(from_date).date()

        if not to_date:
            to_date = timezone.now().date()
        else:
            to_date = datetime.fromisoformat(to_date).date()

        if report_type == 'timeseries':
            return self._get_timeseries(from_date, to_date, granularity)
        elif report_type == 'by-gateway':
            return self._get_by_gateway(from_date, to_date)
        elif report_type == 'top-courses':
            return self._get_top_courses(from_date, to_date)
        else:
            return Response({'error': 'Invalid report type'}, status=status.HTTP_400_BAD_REQUEST)

    def _get_timeseries(self, from_date, to_date, granularity):
        """Get revenue time series"""
        current = from_date
        points = []

        while current <= to_date:
            next_date = current + timedelta(days=1)
            if granularity == 'week':
                next_date = current + timedelta(days=7)
            elif granularity == 'month':
                next_date = (current.replace(day=28) + timedelta(days=4)).replace(day=1)

            payments = Payment.objects.filter(
                created_at__date__gte=current,
                created_at__date__lt=next_date,
                status='paid'
            )

            gross = payments.aggregate(total=Sum('amount'))['total'] or 0
            refunds = payments.filter(status='refunded').aggregate(total=Sum('amount'))['total'] or 0
            fees = gross * 0.03  # Placeholder
            net = gross - fees - refunds

            points.append({
                'date': current.isoformat(),
                'gross': float(gross),
                'net': float(net),
                'refunds': float(refunds)
            })

            current = next_date

        return Response(points, status=status.HTTP_200_OK)

    def _get_by_gateway(self, from_date, to_date):
        """Get revenue by gateway"""
        payments = Payment.objects.filter(
            created_at__date__gte=from_date,
            created_at__date__lte=to_date,
            status='paid'
        )

        gateways = {}
        for payment in payments:
            gateway = payment.metadata.get('gateway', 'Unknown') if payment.metadata else 'Unknown'
            if gateway not in gateways:
                gateways[gateway] = 0
            gateways[gateway] += float(payment.amount)

        result = [{'gateway': k, 'amount': v} for k, v in gateways.items()]
        return Response(result, status=status.HTTP_200_OK)

    def _get_top_courses(self, from_date, to_date):
        """Get top courses by revenue"""
        payments = Payment.objects.filter(
            created_at__date__gte=from_date,
            created_at__date__lte=to_date,
            status='paid'
        ).select_related('plan')

        course_revenue = {}
        for payment in payments:
            if payment.plan:
                course_id = str(payment.plan.id)
                if course_id not in course_revenue:
                    course_revenue[course_id] = {
                        'courseId': course_id,
                        'title': payment.plan.name,
                        'teacher': 'N/A',
                        'gross': 0,
                        'net': 0,
                        'orders': 0
                    }
                course_revenue[course_id]['gross'] += float(payment.amount)
                course_revenue[course_id]['orders'] += 1

        # Calculate net
        for course_id, data in course_revenue.items():
            fees = data['gross'] * 0.03
            data['net'] = data['gross'] - fees

        result = sorted(course_revenue.values(), key=lambda x: x['gross'], reverse=True)[:10]
        return Response(result, status=status.HTTP_200_OK)


class AdminUserReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Get user analytics reports"""
        report_type = request.query_params.get('type', 'kpis')  # kpis, timeseries, by-role
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')

        if report_type == 'kpis':
            return self._get_user_kpis(from_date, to_date)
        elif report_type == 'timeseries':
            return self._get_user_timeseries(from_date, to_date)
        elif report_type == 'by-role':
            return self._get_user_by_role()
        else:
            return Response({'error': 'Invalid report type'}, status=status.HTTP_400_BAD_REQUEST)

    def _get_user_kpis(self, from_date, to_date):
        """Get user KPIs"""
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        dau = UserModel.objects.filter(last_login__gte=today_start).count()
        mau = UserModel.objects.filter(last_login__gte=now - timedelta(days=30)).count()

        if from_date:
            from_date = datetime.fromisoformat(from_date).date()
            new_users = UserModel.objects.filter(created_on__date__gte=from_date).count()
        else:
            new_users = UserModel.objects.filter(created_on__gte=now - timedelta(days=7)).count()

        active_users = UserModel.objects.filter(last_login__gte=now - timedelta(days=7)).count()

        return Response({
            'dau': dau,
            'mau': mau,
            'newUsers': new_users,
            'activeUsers': active_users
        }, status=status.HTTP_200_OK)

    def _get_user_timeseries(self, from_date, to_date):
        """Get user time series"""
        if not from_date:
            from_date = (timezone.now() - timedelta(days=30)).date()
        else:
            from_date = datetime.fromisoformat(from_date).date()

        if not to_date:
            to_date = timezone.now().date()
        else:
            to_date = datetime.fromisoformat(to_date).date()

        current = from_date
        points = []

        while current <= to_date:
            next_date = current + timedelta(days=1)
            day_start = timezone.make_aware(datetime.combine(current, datetime.min.time()))
            day_end = timezone.make_aware(datetime.combine(next_date, datetime.min.time()))

            dau = UserModel.objects.filter(
                last_login__gte=day_start,
                last_login__lt=day_end
            ).count()

            new_users = UserModel.objects.filter(
                created_on__gte=day_start,
                created_on__lt=day_end
            ).count()

            points.append({
                'date': current.isoformat(),
                'dau': dau,
                'newUsers': new_users
            })

            current = next_date

        return Response(points, status=status.HTTP_200_OK)

    def _get_user_by_role(self):
        """Get user count by role"""
        roles = UserModel.objects.values('role').annotate(count=Count('id'))
        result = [{'role': r['role'], 'count': r['count']} for r in roles]
        return Response(result, status=status.HTTP_200_OK)


class AdminLearningReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Get learning analytics reports"""
        report_type = request.query_params.get('type', 'kpis')  # kpis, completion, score-by-subject, at-risk
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')

        if report_type == 'kpis':
            # Placeholder - need progress/learning models
            return Response({
                'avgCompletion': 62,
                'avgScore': 74,
                'avgTimeSpentMin': 38
            }, status=status.HTTP_200_OK)
        elif report_type == 'completion':
            # Placeholder
            return Response([], status=status.HTTP_200_OK)
        elif report_type == 'score-by-subject':
            # Placeholder
            return Response([], status=status.HTTP_200_OK)
        elif report_type == 'at-risk':
            # Placeholder
            return Response([], status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid report type'}, status=status.HTTP_400_BAD_REQUEST)


class AdminContentReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Get content analytics reports"""
        report_type = request.query_params.get('type', 'kpis')  # kpis, views-by-subject, top
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')

        if report_type == 'kpis':
            total_published = Course.objects.filter(published=True).count()
            # Placeholder for enrollments and rating
            return Response({
                'totalPublished': total_published,
                'totalEnrollments': 0,  # Placeholder
                'avgRating': 4.3  # Placeholder
            }, status=status.HTTP_200_OK)
        elif report_type == 'views-by-subject':
            # Placeholder
            return Response([], status=status.HTTP_200_OK)
        elif report_type == 'top':
            # Placeholder
            return Response([], status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid report type'}, status=status.HTTP_400_BAD_REQUEST)



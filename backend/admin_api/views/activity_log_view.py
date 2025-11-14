from datetime import datetime, timedelta
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from admin_api.permissions import IsAdmin
from custom_account.models import UserModel


class AdminActivityLogView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Get activity logs"""
        # Placeholder - in production, query actual activity log model
        # For now, use user login history as placeholder

        q = request.query_params.get('q', '')
        action = request.query_params.get('action')
        user_id = request.query_params.get('userId')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 20))

        # Use user model as placeholder for activity logs
        queryset = UserModel.objects.all()

        if q:
            queryset = queryset.filter(
                Q(email__icontains=q) |
                Q(username__icontains=q)
            )

        if user_id:
            queryset = queryset.filter(id=user_id)

        # Paginate
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)

        # Serialize as activity logs
        items = []
        for user in page_obj:
            items.append({
                'id': str(user.id),
                'userId': str(user.id),
                'userEmail': user.email,
                'action': 'login',  # Placeholder
                'ip': '127.0.0.1',  # Placeholder
                'userAgent': 'Mozilla/5.0',  # Placeholder
                'timestamp': user.last_login.isoformat() if user.last_login else user.created_on.isoformat(),
                'status': 'success',  # Placeholder
                'details': {}  # Placeholder
            })

        return Response({
            'items': items,
            'total': paginator.count
        }, status=status.HTTP_200_OK)



from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
import logging

from student_api.permissions import IsStudent
from activities.models import Notification

logger = logging.getLogger(__name__)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'type', 'category', 'is_read', 'created_at', 'metadata']
        read_only_fields = ['id', 'created_at']


class StudentNotificationsView(APIView):
    """
    GET /api/student/notifications/
    List notifications for the authenticated student
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        try:
            user = request.user
            limit = int(request.query_params.get('limit', 20))
            
            notifications = Notification.objects.filter(
                user=user
            ).order_by('-created_at')[:limit]

            serializer = NotificationSerializer(notifications, many=True)
            return Response({
                'notifications': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error in StudentNotificationsView: {e}", exc_info=True)
            return Response({'error': f'Internal Server Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentNotificationReadView(APIView):
    """
    PATCH /api/student/notifications/<id>/read/
    Mark a notification as read
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def patch(self, request, id):
        try:
            user = request.user
            notification = Notification.objects.get(id=id, user=user)
            notification.is_read = True
            notification.save()
            
            return Response({'success': True}, status=status.HTTP_200_OK)

        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in StudentNotificationReadView: {e}", exc_info=True)
            return Response({'error': f'Internal Server Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentNotificationReadAllView(APIView):
    """
    PATCH /api/student/notifications/read-all/
    Mark all notifications as read
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def patch(self, request):
        try:
            user = request.user
            Notification.objects.filter(user=user, is_read=False).update(is_read=True)
            
            return Response({'success': True}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error in StudentNotificationReadAllView: {e}", exc_info=True)
            return Response({'error': f'Internal Server Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


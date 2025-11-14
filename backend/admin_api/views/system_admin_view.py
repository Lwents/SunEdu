import json
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from admin_api.permissions import IsAdmin


class AdminSystemConfigView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Get system configuration"""
        # Get config from cache or default
        config = cache.get('system_config')
        if not config:
            config = self._get_default_config()

        return Response(config, status=status.HTTP_200_OK)

    def post(self, request):
        """Update system configuration"""
        config = request.data

        # Validate and save to cache (in production, save to database)
        cache.set('system_config', config, timeout=None)

        # Update version
        config['version'] = config.get('version', 0) + 1
        config['updatedBy'] = request.user.email
        config['updatedAt'] = timezone.now().isoformat()

        return Response(config, status=status.HTTP_200_OK)

    def _get_default_config(self):
        """Get default system configuration"""
        return {
            'brand': {
                'siteName': getattr(settings, 'SITE_NAME', 'SunEdu'),
                'language': 'vi',
                'timezone': 'Asia/Ho_Chi_Minh',
                'currency': 'VND',
                'logoUrl': ''
            },
            'domainEmail': {
                'domain': getattr(settings, 'ALLOWED_HOSTS', ['localhost'])[0],
                'forceHttps': True,
                'hsts': True,
                'smtp': {
                    'host': getattr(settings, 'EMAIL_HOST', ''),
                    'port': getattr(settings, 'EMAIL_PORT', 587),
                    'username': getattr(settings, 'EMAIL_HOST_USER', ''),
                    'passwordMasked': bool(getattr(settings, 'EMAIL_HOST_PASSWORD', '')),
                    'senderName': getattr(settings, 'DEFAULT_FROM_NAME', ''),
                    'fromEmail': getattr(settings, 'DEFAULT_FROM_EMAIL', '')
                },
                'spf': {'status': 'unknown'},
                'dkim': {'status': 'unknown'},
                'dmarc': {'status': 'unknown'}
            },
            'authSession': {
                'idleTimeoutMin': 30,
                'maxSessionHours': 24,
                'rememberMeDays': 14,
                'ssoGoogleEnabled': False,
                'googleClientId': '',
                'twoFAEnforce': {'admin': True, 'teacher': False},
                'passwordPolicy': {
                    'minLength': 8,
                    'requireNumbers': True,
                    'requireSymbols': True
                },
                'singleDeviceOnly': True
            },
            'backup': {
                'schedule': 'daily',
                'retentionDays': 30,
                'rpoMinutes': 15,
                'rtoMinutes': 120,
                'encrypted': True
            },
            'maintenance': {
                'enabled': False,
                'window': {
                    'dayOfWeek': 0,
                    'start': '01:00',
                    'end': '03:00'
                }
            },
            'integrations': {
                'payments': {
                    'momo': True,
                    'vnpay': True,
                    'qr': True,
                    'bank': True
                },
                'analytics': {
                    'ga4MeasurementId': ''
                },
                'zoom': {
                    'enabled': False
                },
                'storage': {
                    'provider': 'local',
                    'bucket': '',
                    'region': ''
                }
            },
            'logging': {
                'level': 'info',
                'retentionDays': 90,
                'traceIdEnabled': True
            },
            'version': 0,
            'updatedBy': '',
            'updatedAt': timezone.now().isoformat()
        }


class AdminSystemBackupView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """List backups"""
        # Placeholder - in production, query backup storage
        backups = cache.get('system_backups', [])
        return Response(backups, status=status.HTTP_200_OK)

    def post(self, request):
        """Create backup"""
        backup_type = request.data.get('type', 'manual')

        # Placeholder - in production, trigger backup job
        backup_id = f"backup_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
        backup = {
            'id': backup_id,
            'createdAt': timezone.now().isoformat(),
            'sizeMB': 0,  # Placeholder
            'notes': f'Manual backup - {backup_type}'
        }

        backups = cache.get('system_backups', [])
        backups.insert(0, backup)
        cache.set('system_backups', backups[:10], timeout=None)  # Keep last 10

        return Response(backup, status=status.HTTP_201_CREATED)


class AdminSystemRestoreView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        """Restore from backup"""
        backup_id = request.data.get('backupId')

        if not backup_id:
            return Response({'error': 'backupId required'}, status=status.HTTP_400_BAD_REQUEST)

        # Placeholder - in production, trigger restore job
        return Response({
            'success': True,
            'message': f'Restore job queued for {backup_id}'
        }, status=status.HTTP_200_OK)


class AdminSystemAuditView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Get config audit log"""
        # Placeholder - in production, query audit log table
        audits = cache.get('system_config_audits', [])
        return Response(audits, status=status.HTTP_200_OK)


class AdminSystemTestEmailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        """Send test email"""
        email = request.data.get('email')

        if not email:
            return Response({'error': 'email required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            send_mail(
                subject='Test Email from SunEdu',
                message='This is a test email from the SunEdu admin panel.',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
                recipient_list=[email],
                fail_silently=False
            )
            return Response({'success': True, 'message': 'Test email sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


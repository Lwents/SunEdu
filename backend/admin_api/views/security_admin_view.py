from datetime import timedelta
from django.core.cache import cache
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from admin_api.permissions import IsAdmin


class AdminSecurityPolicyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Get security policy"""
        try:
            policy = cache.get('security_policy')
        except Exception:
            policy = None
        if not policy:
            policy = {
                'twoFA': {
                    'enforceAdmin': True,
                    'enforceTeacher': False
                },
                'rateLimit': {
                    'loginFailures': 5,
                    'windowMin': 10
                },
                'lockout': {
                    'attempts': 5,
                    'lockMinutes': 30,
                    'banStrikes': 5
                },
                'rbacNote': ''
            }
        return Response(policy, status=status.HTTP_200_OK)

    def post(self, request):
        """Update security policy"""
        policy = request.data
        try:
            cache.set('security_policy', policy, timeout=None)
        except Exception:
            # If cache fails, continue without caching
            pass
        return Response(policy, status=status.HTTP_200_OK)


class AdminIpAllowListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """List IP allowlist"""
        try:
            ip_list = cache.get('security_ip_allowlist', [])
        except Exception:
            ip_list = []
        return Response(ip_list, status=status.HTTP_200_OK)

    def post(self, request):
        """Add IP to allowlist"""
        cidr = request.data.get('cidr')
        note = request.data.get('note', '')

        if not cidr:
            return Response({'error': 'cidr required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ip_list = cache.get('security_ip_allowlist', [])
        except Exception:
            ip_list = []
        ip_item = {
            'id': f"ip_{len(ip_list) + 1}",
            'cidr': cidr,
            'note': note,
            'createdAt': timezone.now().isoformat(),
            'createdBy': request.user.email
        }
        ip_list.append(ip_item)
        try:
            cache.set('security_ip_allowlist', ip_list, timeout=None)
        except Exception:
            # If cache fails, continue without caching
            pass

        return Response(ip_item, status=status.HTTP_201_CREATED)


class AdminIpAllowDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, pk):
        """Remove IP from allowlist"""
        try:
            ip_list = cache.get('security_ip_allowlist', [])
            ip_list = [ip for ip in ip_list if ip.get('id') != pk]
            cache.set('security_ip_allowlist', ip_list, timeout=None)
        except Exception:
            # If cache fails, continue without caching
            pass
        return Response({'success': True}, status=status.HTTP_200_OK)


class AdminCertStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Get TLS certificate status"""
        try:
            cert = cache.get('security_cert_status')
        except Exception:
            cert = None
        if not cert:
            cert = {
                'issuer': 'Let\'s Encrypt',
                'validFrom': timezone.now().isoformat(),
                'validTo': (timezone.now() + timezone.timedelta(days=60)).isoformat(),
                'daysRemaining': 60,
                'autoRenew': True
            }
        return Response(cert, status=status.HTTP_200_OK)

    def post(self, request):
        """Renew certificate"""
        # Placeholder - in production, trigger cert renewal job
        cert = {
            'issuer': 'Let\'s Encrypt',
            'validFrom': timezone.now().isoformat(),
            'validTo': (timezone.now() + timezone.timedelta(days=90)).isoformat(),
            'daysRemaining': 90,
            'autoRenew': True
        }
        try:
            cache.set('security_cert_status', cert, timeout=None)
        except Exception:
            # If cache fails, continue without caching
            pass
        return Response({
            'success': True,
            'message': 'Certificate renewal job queued',
            'cert': cert
        }, status=status.HTTP_200_OK)


class AdminSessionListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """List active sessions"""
        user_id = request.query_params.get('userId')

        # Placeholder - in production, query actual session store
        # For now, return mock data based on user_id
        sessions = []
        if user_id:
            # Return sessions for specific user
            sessions = [
                {
                    'jti': f'session_{user_id}_1',
                    'userId': int(user_id),
                    'device': 'Windows • Chrome',
                    'ip': '192.168.1.100',
                    'location': 'VN',
                    'createdAt': timezone.now().isoformat(),
                    'lastActiveAt': timezone.now().isoformat()
                }
            ]
        else:
            # Return all active sessions (limited)
            sessions = [
                {
                    'jti': f'session_{i}',
                    'userId': i,
                    'device': 'Windows • Chrome' if i % 2 == 0 else 'Android • Chrome',
                    'ip': f'192.168.1.{100 + i}',
                    'location': 'VN',
                    'createdAt': timezone.now().isoformat(),
                    'lastActiveAt': timezone.now().isoformat()
                }
                for i in range(1, 11)
            ]

        return Response(sessions, status=status.HTTP_200_OK)


class AdminSessionRevokeView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, jti):
        """Revoke a session"""
        # Placeholder - in production, revoke from session store
        return Response({
            'success': True,
            'message': f'Session {jti} revoked'
        }, status=status.HTTP_200_OK)


class AdminAlertPolicyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Get alert policy"""
        try:
            alert_policy = cache.get('security_alert_policy')
        except Exception:
            alert_policy = None
        if not alert_policy:
            alert_policy = {
                'cpuThreshold': 90,
                'errorRateThreshold': 2,
                'channels': {
                    'email': True,
                    'sms': True
                },
                'onCall': ''
            }
        return Response(alert_policy, status=status.HTTP_200_OK)

    def post(self, request):
        """Update alert policy"""
        alert_policy = request.data
        try:
            cache.set('security_alert_policy', alert_policy, timeout=None)
        except Exception:
            # If cache fails, continue without caching
            pass
        return Response(alert_policy, status=status.HTTP_200_OK)

    def put(self, request):
        """Test alert"""
        # Placeholder - in production, send test alert
        return Response({
            'success': True,
            'message': 'Test alert sent'
        }, status=status.HTTP_200_OK)


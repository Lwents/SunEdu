from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from student_api.permissions import IsStudent
from custom_account.models import UserModel


class StudentProfileView(APIView):
    """
    GET /api/student/account/profile/
    PUT /api/student/account/profile/
    Returns or updates student profile
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        """Get student profile"""
        user = request.user
        
        profile_data = {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'fullName': user.get_full_name() or user.username,
            'phone': getattr(user, 'phone', ''),
            'avatar': getattr(user, 'avatar', None),
            'role': getattr(user, 'role', 'student'),
            'dateJoined': user.date_joined.isoformat() if user.date_joined else None,
        }
        
        return Response(profile_data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update student profile"""
        user = request.user
        
        # Update allowed fields
        if 'firstName' in request.data:
            user.first_name = request.data['firstName']
        if 'lastName' in request.data:
            user.last_name = request.data['lastName']
        if 'email' in request.data:
            user.email = request.data['email']
        if 'phone' in request.data:
            setattr(user, 'phone', request.data['phone'])
        
        user.save()
        
        profile_data = {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'fullName': user.get_full_name() or user.username,
            'phone': getattr(user, 'phone', ''),
            'avatar': getattr(user, 'avatar', None),
            'role': getattr(user, 'role', 'student'),
            'dateJoined': user.date_joined.isoformat() if user.date_joined else None,
        }
        
        return Response(profile_data, status=status.HTTP_200_OK)


class StudentChangePasswordView(APIView):
    """
    POST /api/student/account/change-password/
    Changes student password
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        """Change password"""
        user = request.user
        
        old_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')
        
        if not old_password or not new_password:
            return Response(
                {'detail': 'oldPassword and newPassword are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check old password
        if not user.check_password(old_password):
            return Response(
                {'detail': 'Incorrect old password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate new password
        try:
            validate_password(new_password, user)
        except DjangoValidationError as e:
            return Response(
                {'detail': '; '.join(e.messages)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Update session to prevent logout
        update_session_auth_hash(request, user)
        
        return Response(
            {'detail': 'Password changed successfully'},
            status=status.HTTP_200_OK
        )


class StudentParentViewView(APIView):
    """
    GET /api/student/account/parent/
    PUT /api/student/account/parent/
    Returns or updates parent information for student
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        """Get parent information"""
        user = request.user
        
        # Parent info might be stored in user profile or separate model
        # For now, return empty/default structure
        parent_data = {
            'name': getattr(user, 'parent_name', ''),
            'email': getattr(user, 'parent_email', ''),
            'phone': getattr(user, 'parent_phone', ''),
            'relationship': getattr(user, 'parent_relationship', ''),
        }
        
        return Response(parent_data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update parent information"""
        user = request.user
        
        # Update parent fields if they exist on user model
        if 'name' in request.data:
            setattr(user, 'parent_name', request.data['name'])
        if 'email' in request.data:
            setattr(user, 'parent_email', request.data['email'])
        if 'phone' in request.data:
            setattr(user, 'parent_phone', request.data['phone'])
        if 'relationship' in request.data:
            setattr(user, 'parent_relationship', request.data['relationship'])
        
        user.save()
        
        parent_data = {
            'name': getattr(user, 'parent_name', ''),
            'email': getattr(user, 'parent_email', ''),
            'phone': getattr(user, 'parent_phone', ''),
            'relationship': getattr(user, 'parent_relationship', ''),
        }
        
        return Response(parent_data, status=status.HTTP_200_OK)



#!/usr/bin/env python
"""
Script to create or update Django superuser
Usage: python create_superuser.py [username] [password] [email]
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_or_update_superuser(username='admin', password='lekien2004', email='admin@example.com'):
    """Create or update a superuser"""
    try:
        user = User.objects.filter(username=username).first()
        
        if user:
            print(f"User '{username}' already exists. Updating...")
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            if hasattr(user, 'email'):
                user.email = email
            if hasattr(user, 'role'):
                user.role = 'admin'
            user.save()
            print(f"✓ Updated user '{username}' successfully")
        else:
            print(f"Creating new superuser '{username}'...")
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_superuser=True,
                is_staff=True,
                is_active=True
            )
            if hasattr(user, 'role'):
                user.role = 'admin'
                user.save()
            print(f"✓ Created superuser '{username}' successfully (ID: {user.id})")
        
        print(f"\n=== User Details ===")
        print(f"Username: {user.username}")
        print(f"Email: {getattr(user, 'email', 'N/A')}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Is Staff: {user.is_staff}")
        print(f"Is Active: {user.is_active}")
        if hasattr(user, 'role'):
            print(f"Role: {user.role}")
        
        return user
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    username = sys.argv[1] if len(sys.argv) > 1 else 'admin'
    password = sys.argv[2] if len(sys.argv) > 2 else 'lekien2004'
    email = sys.argv[3] if len(sys.argv) > 3 else 'admin@example.com'
    
    create_or_update_superuser(username, password, email)



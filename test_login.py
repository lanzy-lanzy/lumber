#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
django.setup()

from django.contrib.auth import authenticate
from core.models import CustomUser

# Try to authenticate as lanzy
user = authenticate(username='lanzy', password='lanzy123456')
print(f"Authentication result: {user}")

if user:
    print(f"User: {user.username}")
    print(f"User type: {user.user_type}")
    print(f"Is active: {user.is_active}")
    print(f"Is customer: {user.is_customer()}")
else:
    print("Authentication failed")
    
    # Check if user exists
    try:
        user = CustomUser.objects.get(username='lanzy')
        print(f"User exists: {user}")
        print(f"Is active: {user.is_active}")
        print(f"Password check: {user.check_password('lanzy123456')}")
    except CustomUser.DoesNotExist:
        print("User lanzy does not exist")

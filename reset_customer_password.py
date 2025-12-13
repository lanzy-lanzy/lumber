#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
django.setup()

from core.models import CustomUser

# Reset lanzy password to 'password123'
user = CustomUser.objects.get(username='lanzy')
user.set_password('password123')
user.save()
print(f"Reset password for {user.username} to 'password123'")

# Verify it works
from django.contrib.auth import authenticate
auth_user = authenticate(username='lanzy', password='password123')
print(f"Authentication test: {auth_user}")

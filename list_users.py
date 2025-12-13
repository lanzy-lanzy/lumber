#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
django.setup()

from core.models import CustomUser

print("All users:")
for user in CustomUser.objects.all():
    print(f"  Username: {user.username}, Type: {user.user_type}, Name: {user.get_full_name()}")

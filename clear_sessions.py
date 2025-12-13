#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
django.setup()

from django.contrib.sessions.models import Session

# Delete all sessions
deleted_count, _ = Session.objects.all().delete()
print(f"Cleared {deleted_count} sessions")

#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
django.setup()

from django.urls import reverse

try:
    url = reverse('customer-dashboard')
    print(f"customer-dashboard reverses to: {url}")
except Exception as e:
    print(f"Error reversing customer-dashboard: {e}")

try:
    url = reverse('dashboard')
    print(f"dashboard reverses to: {url}")
except Exception as e:
    print(f"Error reversing dashboard: {e}")

# List all URL patterns
from django.urls import get_resolver
resolver = get_resolver()
print("\nAll URL patterns:")
for pattern in resolver.url_patterns:
    print(f"  {pattern}")

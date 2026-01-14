#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
django.setup()

from app_sales.models import Customer
from django.db.models import Count

# Find duplicate emails
duplicates = Customer.objects.values('email').annotate(count=Count('id')).filter(count__gt=1, email__isnull=False).exclude(email='')
print("Duplicate emails:")
for dup in duplicates:
    print(f"  Email: {dup['email']} - Count: {dup['count']}")
    customers = Customer.objects.filter(email=dup['email']).order_by('created_at')
    for c in customers:
        print(f"    ID: {c.id}, Name: {c.name}, Created: {c.created_at}")

#!/usr/bin/env python
"""
Script to fix duplicate customers in the database
Run with: python manage.py shell < fix_duplicate_customers.py
"""
import os
import django

# Only setup if not already done
if not os.environ.get('DJANGO_SETUP_DONE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
    django.setup()

from app_sales.models import Customer
from django.db.models import Count

# Find customers with duplicate emails
duplicates = Customer.objects.values('email').annotate(
    count=Count('id')
).filter(count__gt=1, email__isnull=False).exclude(email='')

print(f"Found {duplicates.count()} emails with duplicates\n")

for dup in duplicates:
    email = dup['email']
    customers = Customer.objects.filter(email=email).order_by('created_at')
    
    # Keep the first (oldest) customer, delete the rest
    to_keep = customers.first()
    to_delete = customers.exclude(id=to_keep.id)
    
    print(f"Email: {email}")
    print(f"  Keeping: ID {to_keep.id} - {to_keep.name} (created: {to_keep.created_at})")
    print(f"  Deleting {to_delete.count()} duplicate(s):")
    for cust in to_delete:
        print(f"    - ID {cust.id} - {cust.name} (created: {cust.created_at})")
    
    to_delete.delete()
    print()

print("Duplicate cleanup complete!")

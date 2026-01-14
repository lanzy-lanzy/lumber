#!/usr/bin/env python
"""
Manual script to fix duplicate customers and reassign their orders.

Run this in Django shell:
    python manage.py shell < manual_duplicate_customer_fix.py

Or inside a Django shell:
    exec(open('manual_duplicate_customer_fix.py').read())
"""

from app_sales.models import Customer
from app_lumbering_service.models import LumberingServiceOrder
from app_sales.notification_models import OrderNotification, OrderConfirmation
from django.db.models import Count

print("=" * 60)
print("DUPLICATE CUSTOMER FIX")
print("=" * 60)

# Find customers with duplicate emails
duplicates = Customer.objects.values('email').annotate(
    count=Count('id')
).filter(count__gt=1, email__isnull=False).exclude(email='')

if not duplicates.exists():
    print("\nNo duplicate customers found!")
    print("The database is clean.")
else:
    print(f"\nFound {duplicates.count()} email(s) with duplicate customers\n")
    
    for dup in duplicates:
        email = dup['email']
        customers = Customer.objects.filter(email=email).order_by('created_at')
        
        # Keep the first (oldest) customer, delete the rest
        to_keep = customers.first()
        to_delete = customers.exclude(id=to_keep.id)
        
        print(f"Email: {email}")
        print(f"  Keeping: ID {to_keep.id} - {to_keep.name} (created: {to_keep.created_at.strftime('%Y-%m-%d %H:%M:%S')})")
        print(f"  Deleting {to_delete.count()} duplicate(s):")
        
        # Count related objects for each duplicate
        for cust in to_delete:
            lso_count = LumberingServiceOrder.objects.filter(customer=cust).count()
            notif_count = OrderNotification.objects.filter(customer=cust).count()
            conf_count = OrderConfirmation.objects.filter(customer=cust).count()
            
            print(f"    - ID {cust.id} - {cust.name}")
            print(f"      Related: {lso_count} Lumbering Orders, {notif_count} Notifications, {conf_count} Confirmations")
        
        # Reassign all related objects before deleting
        print(f"\n  Reassigning related objects...")
        for cust in to_delete:
            # Count before reassignment
            lso_count = LumberingServiceOrder.objects.filter(customer=cust).count()
            notif_count = OrderNotification.objects.filter(customer=cust).count()
            conf_count = OrderConfirmation.objects.filter(customer=cust).count()
            
            # Reassign lumbering service orders
            if lso_count > 0:
                LumberingServiceOrder.objects.filter(customer=cust).update(customer=to_keep)
                print(f"    ✓ Reassigned {lso_count} Lumbering Service Orders")
            
            # Reassign notifications
            if notif_count > 0:
                OrderNotification.objects.filter(customer=cust).update(customer=to_keep)
                print(f"    ✓ Reassigned {notif_count} Order Notifications")
            
            # Reassign order confirmations
            if conf_count > 0:
                OrderConfirmation.objects.filter(customer=cust).update(customer=to_keep)
                print(f"    ✓ Reassigned {conf_count} Order Confirmations")
        
        # Delete the duplicates
        deleted_count = to_delete.count()
        to_delete.delete()
        print(f"\n  ✓ Deleted {deleted_count} duplicate customer(s)")
        print()

print("=" * 60)
print("FIX COMPLETE")
print("=" * 60)
print("\nNow run migrations if not already done:")
print("  python manage.py migrate")
print("\nThen test checkout functionality.")

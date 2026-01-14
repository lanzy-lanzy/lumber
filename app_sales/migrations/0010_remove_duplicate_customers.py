# Generated migration to remove duplicate customers and add unique constraint

from django.db import migrations, models
from django.db.models import Count


def remove_duplicates(apps, schema_editor):
    """Remove duplicate customers, keeping the oldest one"""
    Customer = apps.get_model('app_sales', 'Customer')
    LumberingServiceOrder = apps.get_model('app_lumbering_service', 'LumberingServiceOrder')
    OrderNotification = apps.get_model('app_sales', 'OrderNotification')
    OrderConfirmation = apps.get_model('app_sales', 'OrderConfirmation')
    
    # Find customers with duplicate emails
    duplicates = Customer.objects.values('email').annotate(
        count=Count('id')
    ).filter(count__gt=1, email__isnull=False).exclude(email='')
    
    for dup in duplicates:
        email = dup['email']
        customers = Customer.objects.filter(email=email).order_by('created_at')
        
        # Keep the first (oldest) customer, delete the rest
        to_keep = customers.first()
        to_delete = customers.exclude(id=to_keep.id)
        
        print(f"Keeping customer {to_keep.id} ({to_keep.name}) for email {email}")
        print(f"Deleting {to_delete.count()} duplicate(s)")
        
        # Reassign all related objects before deleting
        for cust in to_delete:
            # Reassign lumbering service orders
            LumberingServiceOrder.objects.filter(customer=cust).update(customer=to_keep)
            # Reassign notifications
            OrderNotification.objects.filter(customer=cust).update(customer=to_keep)
            # Reassign order confirmations
            OrderConfirmation.objects.filter(customer=cust).update(customer=to_keep)
        
        to_delete.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app_sales', '0009_salesorder_order_source'),
    ]

    operations = [
        migrations.RunPython(remove_duplicates),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]

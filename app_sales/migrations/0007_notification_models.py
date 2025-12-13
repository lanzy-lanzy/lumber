# Generated migration for notification models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_sales', '0006_alter_salesorder_customer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(
                    choices=[
                        ('order_confirmed', 'Order Confirmed'),
                        ('ready_for_pickup', 'Ready for Pickup'),
                        ('payment_pending', 'Payment Pending'),
                        ('payment_completed', 'Payment Completed'),
                        ('order_cancelled', 'Order Cancelled'),
                        ('order_delayed', 'Order Delayed'),
                    ],
                    max_length=30,
                )),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='app_sales.customer')),
                ('sales_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='app_sales.salesorder')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[
                        ('created', 'Created'),
                        ('confirmed', 'Confirmed by Admin'),
                        ('ready_for_pickup', 'Ready for Pickup'),
                        ('picked_up', 'Picked Up'),
                        ('cancelled', 'Cancelled'),
                    ],
                    default='created',
                    max_length=30,
                )),
                ('estimated_pickup_date', models.DateField(blank=True, null=True)),
                ('actual_pickup_date', models.DateField(blank=True, null=True)),
                ('is_payment_complete', models.BooleanField(default=False)),
                ('payment_completed_at', models.DateTimeField(blank=True, null=True)),
                ('confirmed_at', models.DateTimeField(blank=True, null=True)),
                ('ready_at', models.DateTimeField(blank=True, null=True)),
                ('picked_up_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_confirmations_created', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_confirmations', to='app_sales.customer')),
                ('sales_order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='confirmation', to='app_sales.salesorder')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='ordernotification',
            index=models.Index(fields=['customer', '-created_at'], name='app_sales_o_custome_idx'),
        ),
        migrations.AddIndex(
            model_name='ordernotification',
            index=models.Index(fields=['is_read', '-created_at'], name='app_sales_o_is_read_idx'),
        ),
        migrations.AddIndex(
            model_name='ordernotification',
            index=models.Index(fields=['notification_type', '-created_at'], name='app_sales_o_notif_type_idx'),
        ),
        migrations.AddIndex(
            model_name='orderconfirmation',
            index=models.Index(fields=['customer', '-created_at'], name='app_sales_oc_custome_idx'),
        ),
        migrations.AddIndex(
            model_name='orderconfirmation',
            index=models.Index(fields=['status', '-created_at'], name='app_sales_oc_status_idx'),
        ),
    ]

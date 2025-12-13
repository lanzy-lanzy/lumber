from django.db import models
from app_sales.models import SalesOrder, Customer
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderNotification(models.Model):
    """Track notifications for sales orders - ready for pickup, payment status, etc"""
    
    NOTIFICATION_TYPES = [
        ('order_confirmed', 'Order Confirmed'),
        ('ready_for_pickup', 'Ready for Pickup'),
        ('payment_pending', 'Payment Pending'),
        ('payment_completed', 'Payment Completed'),
        ('order_cancelled', 'Order Cancelled'),
        ('order_delayed', 'Order Delayed'),
    ]
    
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='notifications')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notifications')
    
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', '-created_at']),
            models.Index(fields=['is_read', '-created_at']),
            models.Index(fields=['notification_type', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.customer.name}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class OrderConfirmation(models.Model):
    """Track order confirmation status - when order is ready for pickup"""
    
    CONFIRMATION_STATUS = [
        ('created', 'Created'),
        ('confirmed', 'Confirmed by Admin'),
        ('ready_for_pickup', 'Ready for Pickup'),
        ('picked_up', 'Picked Up'),
        ('cancelled', 'Cancelled'),
    ]
    
    sales_order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE, related_name='confirmation')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order_confirmations')
    
    status = models.CharField(max_length=30, choices=CONFIRMATION_STATUS, default='created')
    
    # Pickup details
    estimated_pickup_date = models.DateField(null=True, blank=True)
    actual_pickup_date = models.DateField(null=True, blank=True)
    
    # Payment status
    is_payment_complete = models.BooleanField(default=False)
    payment_completed_at = models.DateTimeField(null=True, blank=True)
    
    # Confirmation timestamps
    confirmed_at = models.DateTimeField(null=True, blank=True)
    ready_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_confirmations_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.sales_order.so_number} - {self.get_status_display()}"
    
    def confirm_order(self, estimated_pickup_date=None):
        """Confirm the order is ready"""
        from django.utils import timezone
        self.status = 'confirmed'
        self.confirmed_at = timezone.now()
        if estimated_pickup_date:
            self.estimated_pickup_date = estimated_pickup_date
        self.save()
    
    def mark_ready_for_pickup(self):
        """Mark order as ready for pickup and create notification"""
        from django.utils import timezone
        self.status = 'ready_for_pickup'
        self.ready_at = timezone.now()
        self.save()
        
        # Create notification for customer
        OrderNotification.objects.create(
            sales_order=self.sales_order,
            customer=self.customer,
            notification_type='ready_for_pickup',
            title=f"Your Order {self.sales_order.so_number} is Ready for Pickup!",
            message=f"Good news! Your order {self.sales_order.so_number} is now ready for pickup. "
                   f"Please come to our store to collect your order. "
                   f"Payment status: {'Completed' if self.is_payment_complete else 'Due on pickup'}"
        )

        # Create Delivery record (Move to Delivery Queue)
        from app_delivery.models import Delivery
        Delivery.objects.get_or_create(
            sales_order=self.sales_order,
            defaults={
                'delivery_number': f"DEL-{self.sales_order.so_number.split('-')[-1]}",
                'status': 'pending'
            }
        )
    
    def mark_payment_complete(self):
        """Mark payment as complete"""
        from django.utils import timezone
        self.is_payment_complete = True
        self.payment_completed_at = timezone.now()
        self.save()
        
        # Create notification if order is already ready
        if self.status == 'ready_for_pickup':
            OrderNotification.objects.get_or_create(
                sales_order=self.sales_order,
                customer=self.customer,
                notification_type='payment_completed',
                defaults={
                    'title': f"Payment Received for Order {self.sales_order.so_number}",
                    'message': f"We've received payment for your order {self.sales_order.so_number}. "
                              f"Your order is ready for pickup!"
                }
            )
    
    def mark_picked_up(self):
        """Mark order as picked up by customer"""
        from django.utils import timezone
        self.status = 'picked_up'
        self.picked_up_at = timezone.now()
        self.save()

        # Update Delivery Status to remove from queue
        try:
            from app_delivery.models import Delivery
            delivery = Delivery.objects.get(sales_order=self.sales_order)
            delivery.status = 'delivered'
            delivery.delivered_at = timezone.now()
            delivery.save()
        except Exception:
            pass

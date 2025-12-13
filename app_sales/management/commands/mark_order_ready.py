"""
Management command to mark orders as ready for pickup and notify customers
Usage: python manage.py mark_order_ready [--order-id ORDER_ID] [--all-pending] [--notify]
"""
from django.core.management.base import BaseCommand, CommandError
from app_sales.models import SalesOrder
from app_sales.notification_models import OrderConfirmation
from app_sales.services import OrderConfirmationService


class Command(BaseCommand):
    help = 'Mark sales orders as ready for pickup and notify customers'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--order-id',
            type=int,
            help='Specific sales order ID to mark as ready'
        )
        parser.add_argument(
            '--all-pending',
            action='store_true',
            help='Mark all pending orders as ready for pickup'
        )
        parser.add_argument(
            '--so-number',
            type=str,
            help='Mark order by SO number (e.g., SO-20251213-0001)'
        )
        parser.add_argument(
            '--notify',
            action='store_true',
            default=True,
            help='Send customer notifications (default: True)'
        )
    
    def handle(self, *args, **options):
        order_id = options.get('order_id')
        all_pending = options.get('all_pending')
        so_number = options.get('so_number')
        
        try:
            if order_id:
                self.mark_order_by_id(order_id)
            elif so_number:
                self.mark_order_by_number(so_number)
            elif all_pending:
                self.mark_all_pending()
            else:
                self.stdout.write(self.style.ERROR(
                    'Please provide --order-id, --so-number, or --all-pending'
                ))
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')
    
    def mark_order_by_id(self, order_id):
        """Mark specific order by ID as ready"""
        try:
            confirmation = OrderConfirmation.objects.get(sales_order_id=order_id)
            self.mark_ready(confirmation)
        except OrderConfirmation.DoesNotExist:
            raise CommandError(f'Order confirmation not found for order ID {order_id}')
    
    def mark_order_by_number(self, so_number):
        """Mark specific order by SO number as ready"""
        try:
            sales_order = SalesOrder.objects.get(so_number=so_number)
            confirmation = OrderConfirmation.objects.get(sales_order=sales_order)
            self.mark_ready(confirmation)
        except SalesOrder.DoesNotExist:
            raise CommandError(f'Sales order not found: {so_number}')
        except OrderConfirmation.DoesNotExist:
            raise CommandError(f'Order confirmation not found for: {so_number}')
    
    def mark_all_pending(self):
        """Mark all pending orders as ready"""
        pending = OrderConfirmation.objects.filter(
            status__in=['created', 'confirmed']
        ).select_related('sales_order', 'customer')
        
        count = pending.count()
        if count == 0:
            self.stdout.write(self.style.WARNING('No pending orders to mark as ready'))
            return
        
        self.stdout.write(f'Found {count} pending order(s)')
        for confirmation in pending:
            self.mark_ready(confirmation)
    
    def mark_ready(self, confirmation):
        """Mark order as ready and notify customer"""
        so_number = confirmation.sales_order.so_number
        customer_name = confirmation.customer.name
        
        if confirmation.status in ['ready_for_pickup', 'picked_up']:
            self.stdout.write(self.style.WARNING(
                f'Order {so_number} is already {confirmation.get_status_display()}'
            ))
            return
        
        try:
            confirmation.mark_ready_for_pickup()
            self.stdout.write(self.style.SUCCESS(
                f'✓ Order {so_number} marked as ready for pickup\n'
                f'  Customer: {customer_name}\n'
                f'  Email: {confirmation.customer.email}\n'
                f'  Payment Status: {"Complete" if confirmation.is_payment_complete else "Pending"}\n'
                f'  Notification: Sent'
            ))
        except Exception as e:
            raise CommandError(f'Failed to mark {so_number} as ready: {str(e)}')

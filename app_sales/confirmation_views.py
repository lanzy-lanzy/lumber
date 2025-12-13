"""
API views for order confirmation and notifications
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from app_sales.notification_models import OrderNotification, OrderConfirmation
from app_sales.models import SalesOrder, Customer
from app_sales.services import OrderConfirmationService
from django.shortcuts import get_object_or_404


class OrderConfirmationViewSet(viewsets.ModelViewSet):
    """API endpoint for order confirmations"""
    queryset = OrderConfirmation.objects.all()
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def create_confirmation(self, request):
        """
        Create order confirmation for a sales order
        
        Expected payload:
        {
            "sales_order_id": 1,
            "estimated_pickup_date": "2025-12-20"
        }
        """
        sales_order_id = request.data.get('sales_order_id')
        estimated_pickup_date = request.data.get('estimated_pickup_date')
        
        if not sales_order_id:
            return Response(
                {'error': 'sales_order_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            confirmation = OrderConfirmationService.create_order_confirmation(
                sales_order_id=sales_order_id,
                estimated_pickup_date=estimated_pickup_date,
                created_by=request.user
            )
            return Response({
                'id': confirmation.id,
                'sales_order_id': confirmation.sales_order_id,
                'status': confirmation.status,
                'message': 'Order confirmation created successfully'
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def mark_ready(self, request, pk=None):
        """Mark order as ready for pickup"""
        try:
            confirmation = OrderConfirmationService.confirm_order_ready(
                sales_order_id=pk
            )
            return Response({
                'id': confirmation.id,
                'status': confirmation.status,
                'ready_at': confirmation.ready_at,
                'message': 'Order marked as ready for pickup. Customer has been notified.'
            })
        except OrderConfirmation.DoesNotExist:
            return Response(
                {'error': 'Order confirmation not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def mark_payment_received(self, request, pk=None):
        """Mark payment as received"""
        try:
            confirmation = OrderConfirmationService.mark_payment_received(
                sales_order_id=pk
            )
            return Response({
                'id': confirmation.id,
                'is_payment_complete': confirmation.is_payment_complete,
                'payment_completed_at': confirmation.payment_completed_at,
                'message': 'Payment marked as received. Customer has been notified.'
            })
        except OrderConfirmation.DoesNotExist:
            return Response(
                {'error': 'Order confirmation not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def mark_picked_up(self, request, pk=None):
        """Mark order as picked up by customer"""
        try:
            confirmation = OrderConfirmationService.mark_order_picked_up(
                sales_order_id=pk
            )
            return Response({
                'id': confirmation.id,
                'status': confirmation.status,
                'picked_up_at': confirmation.picked_up_at,
                'message': 'Order marked as picked up'
            })
        except OrderConfirmation.DoesNotExist:
            return Response(
                {'error': 'Order confirmation not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def pending_pickups(self, request):
        """Get all pending pickups for authenticated customer"""
        try:
            customer = Customer.objects.filter(
                email=request.user.email
            ).first()
            
            if not customer:
                return Response({
                    'pending_pickups': [],
                    'count': 0
                })
            
            confirmations = OrderConfirmationService.get_customer_pending_pickups(
                customer.id
            )
            
            data = []
            for conf in confirmations:
                data.append({
                    'id': conf.id,
                    'sales_order_number': conf.sales_order.so_number,
                    'sales_order_id': conf.sales_order_id,
                    'status': conf.status,
                    'total_amount': float(conf.sales_order.total_amount),
                    'balance': float(conf.sales_order.balance),
                    'payment_complete': conf.is_payment_complete,
                    'estimated_pickup': conf.estimated_pickup_date,
                    'ready_since': conf.ready_at,
                })
            
            return Response({
                'pending_pickups': data,
                'count': len(data)
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NotificationViewSet(viewsets.ModelViewSet):
    """API endpoint for order notifications"""
    queryset = OrderNotification.objects.all()
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_notifications(self, request):
        """Get notifications for authenticated customer"""
        try:
            customer = Customer.objects.filter(
                email=request.user.email
            ).first()
            
            if not customer:
                return Response({
                    'notifications': [],
                    'unread_count': 0
                })
            
            notifications = OrderNotification.objects.filter(
                customer=customer
            ).order_by('-created_at')[:20]
            
            unread_count = OrderNotification.objects.filter(
                customer=customer,
                is_read=False
            ).count()
            
            data = []
            for notif in notifications:
                data.append({
                    'id': notif.id,
                    'type': notif.notification_type,
                    'title': notif.title,
                    'message': notif.message,
                    'is_read': notif.is_read,
                    'created_at': notif.created_at,
                    'sales_order_number': notif.sales_order.so_number if notif.sales_order else None,
                })
            
            return Response({
                'notifications': data,
                'unread_count': unread_count,
                'total_count': len(data)
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a notification as read"""
        try:
            notification = OrderNotification.objects.get(id=pk)
            notification.mark_as_read()
            return Response({
                'id': notification.id,
                'is_read': notification.is_read,
                'read_at': notification.read_at
            })
        except OrderNotification.DoesNotExist:
            return Response(
                {'error': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read for customer"""
        try:
            customer = Customer.objects.filter(
                email=request.user.email
            ).first()
            
            if not customer:
                return Response({
                    'updated_count': 0
                })
            
            unread = OrderNotification.objects.filter(
                customer=customer,
                is_read=False
            )
            count = unread.count()
            
            for notif in unread:
                notif.mark_as_read()
            
            return Response({
                'updated_count': count,
                'message': f'Marked {count} notifications as read'
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications for customer"""
        try:
            customer = Customer.objects.filter(
                email=request.user.email
            ).first()
            
            if not customer:
                return Response({'unread_count': 0})
            
            count = OrderNotification.objects.filter(
                customer=customer,
                is_read=False
            ).count()
            
            return Response({'unread_count': count})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

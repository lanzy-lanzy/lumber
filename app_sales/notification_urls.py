"""
URLs for order notifications and customer order management
"""
from django.urls import path
from app_sales import notification_views

urlpatterns = [
    # Notification views
    path('notifications/', notification_views.customer_notifications, name='notifications'),
    path('notifications/mark-all-read/', notification_views.mark_all_notifications_read, name='mark-all-notifications-read'),
    path('notifications/<int:notification_id>/mark-read/', notification_views.mark_notification_read, name='mark-notification-read'),
    path('notifications/badge-count/', notification_views.notification_badge_count, name='notification-badge-count'),
    
    # Ready orders views
    path('ready-orders/', notification_views.customer_ready_orders, name='ready-orders'),
    
    # Order confirmation detail
    path('orders/<int:confirmation_id>/', notification_views.order_confirmation_detail, name='order-confirmation-detail'),
    path('orders/<int:confirmation_id>/confirm-pickup/', notification_views.confirm_order_pickup, name='confirm-order-pickup'),
]

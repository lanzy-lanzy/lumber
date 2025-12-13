# Order Confirmation Quick Start Guide

## What Was Implemented

✅ **OrderConfirmation Model** - Tracks order status (created → confirmed → ready for pickup → picked up)
✅ **OrderNotification Model** - Sends notifications to customers  
✅ **Context Processor** - Makes notifications available in ALL templates
✅ **API Endpoints** - RESTful endpoints for managing confirmations and notifications
✅ **Admin Interface** - Manage orders and notifications in Django admin
✅ **Frontend Component** - Notification banner for customer dashboard

## Quick Setup

### 1. Run Migration
```bash
python manage.py migrate app_sales
```

### 2. Register API Routes (in `lumber/urls.py`)
```python
from rest_framework.routers import DefaultRouter
from app_sales.confirmation_views import OrderConfirmationViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'confirmations', OrderConfirmationViewSet, basename='confirmation')
router.register(r'notifications', NotificationViewSet, basename='notification')

# In urlpatterns:
urlpatterns = [
    path('api/', include(router.urls)),
]
```

### 3. Add Template to Customer Dashboard
```html
<!-- In your customer dashboard template (e.g., templates/customer/dashboard.html) -->
{% include 'partials/order_notifications.html' %}
```

### 4. Update Sales Order Creation (in `app_sales/views.py`)
When a sales order is created, automatically create a confirmation:

```python
from app_sales.services import OrderConfirmationService
from datetime import datetime, timedelta

# Inside create_order method, after creating sales order:
estimated_date = (datetime.now() + timedelta(days=3)).date()
OrderConfirmationService.create_order_confirmation(
    sales_order_id=so.id,
    estimated_pickup_date=estimated_date,
    created_by=request.user
)
```

## Admin Actions

### In Django Admin

**Manage Confirmations:**
1. Go to Sales → Order Confirmations
2. Search by order number, customer name, or email
3. Filter by status, payment status, or date
4. Edit to change estimated pickup date or notes

**Manage Notifications:**
1. Go to Sales → Order Notifications
2. See all notifications sent to customers
3. Filter by type or read status
4. Search by order number or customer

### Mark Order as Ready (Admin)
```python
# In Django shell or a custom command:
from app_sales.services import OrderConfirmationService

OrderConfirmationService.confirm_order_ready(sales_order_id=5)
# This automatically:
# - Sets status to 'ready_for_pickup'
# - Sets ready_at timestamp
# - Creates notification for customer
```

### Record Payment (Admin)
```python
from app_sales.services import OrderConfirmationService

OrderConfirmationService.mark_payment_received(sales_order_id=5)
# This automatically:
# - Sets is_payment_complete = True
# - Records payment_completed_at timestamp
# - Creates payment notification if order is ready
```

## API Examples

### Get Customer's Pending Pickups
```bash
curl -X GET http://localhost:8000/api/confirmations/pending_pickups/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "pending_pickups": [
    {
      "id": 1,
      "sales_order_number": "SO-20251213-0001",
      "sales_order_id": 1,
      "status": "ready_for_pickup",
      "total_amount": 1500.00,
      "balance": 0.00,
      "payment_complete": true,
      "estimated_pickup": "2025-12-20",
      "ready_since": "2025-12-13T10:30:00Z"
    }
  ],
  "count": 1
}
```

### Get All Notifications
```bash
curl -X GET http://localhost:8000/api/notifications/my_notifications/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "notifications": [
    {
      "id": 1,
      "type": "ready_for_pickup",
      "title": "Your Order SO-20251213-0001 is Ready for Pickup!",
      "message": "Good news! Your order...",
      "is_read": false,
      "created_at": "2025-12-13T10:30:00Z",
      "sales_order_number": "SO-20251213-0001"
    }
  ],
  "unread_count": 3,
  "total_count": 5
}
```

### Mark Order as Ready
```bash
curl -X POST http://localhost:8000/api/confirmations/5/mark_ready/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Mark Payment Received
```bash
curl -X POST http://localhost:8000/api/confirmations/5/mark_payment_received/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Mark Notification as Read
```bash
curl -X POST http://localhost:8000/api/notifications/1/mark_as_read/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Template Variables

In any customer template, you can use:

```django
<!-- Count of unread notifications -->
{{ notification_count }}

<!-- List of unread notifications -->
{% for notif in notifications %}
  {{ notif.title }}
  {{ notif.message }}
{% endfor %}

<!-- Orders ready for pickup -->
{{ ready_pickups_count }}

{% for pickup in ready_pickups %}
  Order: {{ pickup.order_number }}
  Amount: {{ pickup.total_amount }}
  Payment: {{ pickup.payment_complete }}
{% endfor %}
```

## Database Structure

### OrderConfirmation
- Tracks order lifecycle
- Stores pickup dates
- Records payment status
- Maps 1-to-1 with SalesOrder

### OrderNotification  
- Stores all notifications
- Tracks read/unread status
- Maps many-to-1 with SalesOrder and Customer

## Notification Types

| Type | When Triggered | Message |
|------|--------|---------|
| `order_confirmed` | Order created | Order confirmation |
| `ready_for_pickup` | Admin marks ready | Order ready for pickup |
| `payment_pending` | Balance remains | Payment due on pickup |
| `payment_completed` | Payment received | Payment confirmed |
| `order_cancelled` | Order cancelled | Order cancelled |
| `order_delayed` | Delay occurs | Order delayed |

## Customer Experience

**Customer sees:**
1. ✅ Alert banner showing new notifications count
2. ✅ "Order Ready" alert with order details and payment status
3. ✅ Collapsible notification panel
4. ✅ Click to mark notifications as read
5. ✅ Direct link to view full orders

**Customer receives notifications when:**
1. ✅ Order is created
2. ✅ Order is ready for pickup
3. ✅ Payment is received
4. ✅ Order is picked up
5. ✅ Order is cancelled/delayed

## Key Features

✅ **Automatic Notifications** - Triggered by status changes  
✅ **Payment Status Tracking** - Know when payment is complete  
✅ **Pickup Management** - Track pickup dates  
✅ **Read Status** - Customers mark notifications as read  
✅ **Search & Filter** - Admin can find orders easily  
✅ **Context Processor** - No template changes needed  
✅ **RESTful API** - Full API for external integrations  

## Files Added

```
app_sales/
├── notification_models.py       ← New models
├── context_processors.py         ← Context processor
├── confirmation_views.py         ← API endpoints
├── migrations/
│   └── 0007_notification_models.py
└── admin.py (updated)

templates/
└── partials/
    └── order_notifications.html  ← UI component

ORDER_CONFIRMATION_IMPLEMENTATION.md  ← Full docs
ORDER_CONFIRMATION_QUICK_START.md     ← This file

lumber/
└── settings.py (updated)
```

## Testing

```python
# Test in Django shell
python manage.py shell

from app_sales.models import Customer, SalesOrder
from app_sales.notification_models import OrderConfirmation, OrderNotification
from app_sales.services import OrderConfirmationService

# Get a customer and order
customer = Customer.objects.first()
order = SalesOrder.objects.first()

# Create confirmation
conf = OrderConfirmationService.create_order_confirmation(order.id)
print(f"Confirmation created: {conf.status}")

# Check notifications
notifs = OrderNotification.objects.filter(customer=customer)
print(f"Notifications sent: {notifs.count()}")

# Mark as ready
conf = OrderConfirmationService.confirm_order_ready(order.id)
print(f"Order status: {conf.status}")

# Check for new notification
ready_notif = OrderNotification.objects.filter(
    notification_type='ready_for_pickup'
).first()
print(f"Customer notified: {ready_notif.title}")
```

## Troubleshooting

**Q: Notifications not showing in template**
- A: Check if context processor is in settings.py
- Verify customer email matches user email
- Check OrderNotification table in admin

**Q: API returns 404**
- A: Register viewsets in router in urls.py
- Check URL path matches your router

**Q: Can't mark order as ready**
- A: Use `OrderConfirmationService.confirm_order_ready()`
- Verify confirmation exists in database

## Next Steps

1. ✅ Run migration: `python manage.py migrate app_sales`
2. ✅ Register API routes in `lumber/urls.py`
3. ✅ Add template partial to customer dashboard
4. ✅ Update sales order creation to include confirmation
5. ✅ Test in admin: Mark an order as ready, check notification
6. ✅ Test API endpoints with customer account
7. ✅ Deploy to production

## Support Resources

- **Models**: `app_sales/notification_models.py` (50 lines)
- **Services**: `app_sales/services.py` → `OrderConfirmationService` (155 lines)
- **API**: `app_sales/confirmation_views.py` (260 lines)
- **Docs**: `ORDER_CONFIRMATION_IMPLEMENTATION.md` (detailed reference)

All code is documented with docstrings and comments for easy maintenance.

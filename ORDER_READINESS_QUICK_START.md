# Order Readiness & Pickup Notification - Quick Start Guide

## What's Implemented

✅ **Order Confirmation System** - Tracks order status from created → ready → picked up
✅ **Notification System** - Sends notifications to customers when orders are ready
✅ **Context Processor** - Makes notifications available in all templates
✅ **Admin Actions** - Bulk mark orders as ready in Django admin
✅ **Management Command** - CLI tool to manage orders
✅ **API Endpoints** - REST API for order management

---

## How It Works

```
1. Customer places order (SalesOrder created)
   ↓
2. OrderConfirmation created automatically
   ↓
3. Admin marks order ready → Notification sent to customer
   ↓
4. Customer sees "Order Ready for Pickup" notification
   ↓
5. Customer picks up → Mark as picked up
```

---

## 5-Minute Setup

### 1. Run Migrations (if not already done)
```bash
python manage.py migrate
```

### 2. Access Admin Interface
```
Go to: http://localhost:8000/admin
Login with admin credentials
Navigate to: Order Confirmations
```

### 3. Mark Order Ready (Method 1: Admin)
1. Click "Order Confirmations" in admin
2. Select orders with status "Created" or "Confirmed"
3. From dropdown, select "Mark selected orders as ready for pickup and notify customers"
4. Click "Go"
5. Done! Customer notification automatically sent

### 4. Mark Order Ready (Method 2: CLI)
```bash
# Mark by order ID
python manage.py mark_order_ready --order-id=123

# Mark by SO number
python manage.py mark_order_ready --so-number="SO-20251213-0001"

# Mark all pending
python manage.py mark_order_ready --all-pending
```

### 5. Display Notifications in Template
```django
<!-- In any customer dashboard/home template -->

{% if has_ready_pickup_notifications %}
  <div class="alert alert-success">
    <h4>📦 Your Order is Ready!</h4>
    {% for pickup in ready_pickups %}
      <p><strong>Order #{{ pickup.order_number }}</strong></p>
      <p>Total: ₱{{ pickup.total_amount|floatformat:2 }}</p>
      <p>Status: {{ pickup.payment_status }}</p>
    {% endfor %}
  </div>
{% endif %}

{% if notification_count %}
  <div class="notifications">
    <span class="badge">{{ notification_count }} new notifications</span>
  </div>
{% endif %}
```

---

## Key Features

### ✅ Order Confirmation Fields
- **Status**: created → confirmed → ready_for_pickup → picked_up
- **Payment Status**: Complete or pending balance
- **Estimated Pickup Date**: When customer can pick up
- **Timestamps**: When status changed

### ✅ Notification Types
- `order_confirmed` - Order created
- `ready_for_pickup` - Order is ready
- `payment_completed` - Payment received
- `payment_pending` - Waiting for payment

### ✅ Context Variables Available
```python
notifications              # List of unread notifications
notification_count         # Count of unread (0-20)
ready_pickups             # Orders ready with payment info
ready_pickups_count       # Number of orders ready
payment_pending_orders    # Orders awaiting payment
payment_pending_count     # Number with pending payment
has_ready_pickup_notifications    # Boolean
has_payment_notifications         # Boolean
notification_alerts       # Dict: {'ready_for_pickup': 2, ...}
```

---

## Common Tasks

### Mark Single Order Ready
```python
from app_sales.notification_models import OrderConfirmation

confirmation = OrderConfirmation.objects.get(sales_order_id=1)
confirmation.mark_ready_for_pickup()
# ✓ Notification automatically sent to customer
```

### Mark Payment Received
```python
confirmation.mark_payment_complete()
# ✓ Notification automatically sent
```

### Get Unread Notifications
```python
from app_sales.notification_models import OrderNotification

unread = OrderNotification.objects.filter(
    customer_id=1,
    is_read=False
)
for notif in unread:
    print(notif.title, notif.message)
```

### Get Customer's Ready Orders
```python
from app_sales.notification_models import OrderConfirmation

ready = OrderConfirmation.objects.filter(
    customer_id=1,
    status='ready_for_pickup'
)
for conf in ready:
    print(f"{conf.sales_order.so_number} - {conf.sales_order.total_amount}")
```

---

## Admin Actions Reference

### In Django Admin → Order Confirmations

| Action | What Happens |
|--------|--------------|
| Mark ready | Status → ready_for_pickup, sends notification |
| Mark payment | is_payment_complete → True, sends notification |
| Mark picked up | Status → picked_up, records pickup date |

---

## API Quick Reference

### Get All Pending Orders
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/order-confirmations/pending_pickups/
```

### Get Customer Notifications
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/notifications/my_notifications/
```

### Mark Notification as Read
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/notifications/1/mark_as_read/
```

### Mark Order as Ready
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/order-confirmations/1/mark_ready/
```

---

## What Gets Sent to Customer

When order is marked ready, customer receives:

**Notification Title:** "Your Order SO-20251213-0001 is Ready for Pickup!"

**Notification Message:**
```
Good news! Your order SO-20251213-0001 is now ready for pickup. 
Please come to our store to collect your order. 
Payment status: Completed
```

Customer sees this in:
- Notification banner on dashboard
- Context variable in templates
- Notification history
- API endpoint

---

## Database Tables Used

1. **OrderConfirmation** - Tracks order readiness status
2. **OrderNotification** - Stores notifications to customers
3. **SalesOrder** - Original order (payment status linked here)

All automatically populated when:
- Order is created
- Order marked ready
- Payment is received

---

## Troubleshooting

### Notifications not showing?
```python
# Check if notifications exist
from app_sales.notification_models import OrderNotification
notifs = OrderNotification.objects.filter(customer_id=1)
print(f"Total: {notifs.count()}, Unread: {notifs.filter(is_read=False).count()}")

# Check context processor
# In your template: {{ notifications }} should show list
```

### Order not marked ready?
```python
# Check if confirmation exists
from app_sales.notification_models import OrderConfirmation
conf = OrderConfirmation.objects.get(sales_order_id=1)
print(f"Status: {conf.status}, Ready at: {conf.ready_at}")

# Manually mark ready
conf.mark_ready_for_pickup()
```

### Payment not showing?
```python
# Check order details
so = SalesOrder.objects.get(id=1)
print(f"Amount paid: {so.amount_paid}, Balance: {so.balance}")

# Check confirmation
conf = OrderConfirmation.objects.get(sales_order=so)
print(f"Payment complete: {conf.is_payment_complete}")
```

---

## Next Steps

1. ✅ Create customer dashboard showing ready orders
2. ✅ Add email notifications on order ready
3. ✅ Add SMS notifications via Twilio
4. ✅ Create notification preference settings
5. ✅ Add notification bell icon to navbar

---

## Examples

### Show "Order Ready" Alert in Template
```django
{% if has_ready_pickup_notifications %}
  <div class="alert alert-success alert-dismissible fade show">
    <strong>📦 Order Ready!</strong>
    <p>{{ ready_pickups_count }} order(s) ready for pickup</p>
    {% for pickup in ready_pickups %}
      <div class="pickup-card">
        <p>{{ pickup.order_number }} - ₱{{ pickup.total_amount }}</p>
        <p><span class="badge">{{ pickup.payment_status }}</span></p>
      </div>
    {% endfor %}
  </div>
{% endif %}
```

### Show Notification Bell with Count
```django
<a href="/notifications/" class="notification-bell">
  <i class="bell-icon"></i>
  {% if notification_count > 0 %}
    <span class="badge">{{ notification_count }}</span>
  {% endif %}
</a>
```

### Show Payment Due Alert
```django
{% if payment_pending_orders %}
  <div class="alert alert-warning">
    <strong>⚠️ Payment Due</strong>
    {% for order in payment_pending_orders %}
      <p>{{ order.order_number }}: ₱{{ order.balance_due }}</p>
    {% endfor %}
  </div>
{% endif %}
```

---

**Last Updated:** December 13, 2025
**Status:** ✅ Ready for Production

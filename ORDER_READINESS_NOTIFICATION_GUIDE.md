# Order Readiness Notification System Implementation Guide

## Overview
This document explains how to implement and use the order readiness notification system that notifies customers when their orders are ready for pickup and confirms payment status.

## Features Implemented

### 1. **Database Models**
- **OrderConfirmation**: Tracks order status (created → confirmed → ready_for_pickup → picked_up)
- **OrderNotification**: Stores customer notifications for various order events

### 2. **Admin Interface Actions**
Quick actions in Django admin to manage orders:
- Mark orders as ready for pickup (bulk action)
- Mark payment as received (bulk action)
- Mark orders as picked up (bulk action)

### 3. **Management Command**
Command-line tool to mark orders ready and notify customers:

```bash
# Mark specific order by ID
python manage.py mark_order_ready --order-id=123

# Mark specific order by SO number
python manage.py mark_order_ready --so-number="SO-20251213-0001"

# Mark all pending orders as ready
python manage.py mark_order_ready --all-pending

# Notify customers (default: True)
python manage.py mark_order_ready --order-id=123 --notify
```

### 4. **Context Processor for Templates**
The `order_notifications` context processor automatically provides:

```python
# In any template, these variables are available:
- notifications          # List of unread notifications
- notification_count     # Count of unread notifications
- ready_pickups         # Orders ready for pickup with payment info
- ready_pickups_count   # Number of ready pickup orders
- payment_pending_orders # Orders awaiting payment
- payment_pending_count  # Number of orders with pending payment
- has_ready_pickup_notifications  # Boolean flag
- has_payment_notifications        # Boolean flag
- notification_alerts   # Dict with counts by type
```

### 5. **API Endpoints**
RESTful API endpoints for order management:

#### OrderConfirmation endpoints:
```
POST /api/order-confirmations/create_confirmation/
  - Create order confirmation

POST /api/order-confirmations/{id}/mark_ready/
  - Mark order as ready for pickup

POST /api/order-confirmations/{id}/mark_payment_received/
  - Mark payment as received

POST /api/order-confirmations/{id}/mark_picked_up/
  - Mark order as picked up

GET /api/order-confirmations/pending_pickups/
  - Get all pending pickups for authenticated customer
```

#### Notification endpoints:
```
GET /api/notifications/my_notifications/
  - Get all notifications for customer

POST /api/notifications/{id}/mark_as_read/
  - Mark single notification as read

POST /api/notifications/mark_all_as_read/
  - Mark all notifications as read

GET /api/notifications/unread_count/
  - Get count of unread notifications
```

---

## Usage Workflow

### Step 1: Create Sales Order
```python
from app_sales.services import SalesService

so = SalesService.create_sales_order(
    customer_id=1,
    items=[
        {'product_id': 1, 'quantity_pieces': 10},
        {'product_id': 2, 'quantity_pieces': 5},
    ],
    payment_type='cash',
    created_by=request.user
)
# Automatically creates OrderConfirmation and sends "Order Confirmed" notification
```

### Step 2: Process Payment
```python
from app_sales.services import SalesService

so, receipt = SalesService.process_payment(
    sales_order_id=1,
    amount_paid=5000,
    created_by=request.user
)
# Updates payment status in OrderConfirmation
```

### Step 3: Mark Order as Ready for Pickup
#### Option A: Using Admin Interface
1. Go to Django Admin → Order Confirmations
2. Filter orders by status (e.g., "Confirmed")
3. Select orders to mark ready
4. Choose action "Mark selected orders as ready for pickup and notify customers"
5. Click "Go"
6. Customers automatically receive "Ready for Pickup" notification

#### Option B: Using Management Command
```bash
python manage.py mark_order_ready --so-number="SO-20251213-0001"
```

#### Option C: Using API
```bash
curl -X POST http://localhost:8000/api/order-confirmations/1/mark_ready/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Option D: Programmatically
```python
from app_sales.services import OrderConfirmationService

confirmation = OrderConfirmationService.confirm_order_ready(
    sales_order_id=1
)
# Automatically creates "Ready for Pickup" notification
```

### Step 4: Customer Views Notification
When customer logs in, they see:
- Notification banner/alert with message
- Order number, total amount, balance due
- Days ready for pickup
- Payment status (PAID or DUE: amount)

### Step 5: Customer Picks Up Order
```python
from app_sales.services import OrderConfirmationService

confirmation = OrderConfirmationService.mark_order_picked_up(
    sales_order_id=1
)
```

---

## Notification Types

### 1. **order_confirmed**
Sent when: Sales order is created
Message: "Your order {SO_NUMBER} has been successfully created. We will notify you when it's ready for pickup."

### 2. **ready_for_pickup**
Sent when: Admin marks order as ready
Message: "Your order {SO_NUMBER} is now ready for pickup. Please come to our store to collect your order. Payment status: {COMPLETE/DUE}"

### 3. **payment_completed**
Sent when: Payment is received for ready order
Message: "We've received payment for your order {SO_NUMBER}. Your order is ready for pickup!"

### 4. **payment_pending**
Sent when: Order is ready but payment pending
Message: "Your order {SO_NUMBER} is ready for pickup. Payment balance: ₱{AMOUNT}"

---

## Template Integration Examples

### Example 1: Show Ready Pickup Alert
```django
{% if ready_pickups %}
  <div class="alert alert-info">
    <h4>Orders Ready for Pickup!</h4>
    {% for pickup in ready_pickups %}
      <div class="order-card">
        <p>Order #{{ pickup.order_number }}</p>
        <p>Total: ₱{{ pickup.total_amount|floatformat:2 }}</p>
        <p>Status: {{ pickup.payment_status }}</p>
        <p>Ready since: {{ pickup.days_ready }} days ago</p>
      </div>
    {% endfor %}
  </div>
{% endif %}
```

### Example 2: Show Pending Payments
```django
{% if payment_pending_orders %}
  <div class="alert alert-warning">
    <h4>Payment Due</h4>
    {% for order in payment_pending_orders %}
      <div class="payment-card">
        <p>Order #{{ order.order_number }}</p>
        <p>Balance Due: ₱{{ order.balance_due|floatformat:2 }}</p>
      </div>
    {% endfor %}
  </div>
{% endif %}
```

### Example 3: Show Notifications
```django
{% if notifications %}
  <div class="notifications-dropdown">
    <span class="badge">{{ notification_count }}</span>
    {% for notif in notifications %}
      <div class="notification-item">
        <h5>{{ notif.title }}</h5>
        <p>{{ notif.message }}</p>
        <small>{{ notif.created_at|date:"M d, Y H:i" }}</small>
      </div>
    {% endfor %}
  </div>
{% endif %}
```

---

## Service Methods Reference

### SalesService
```python
# Create sales order with auto confirmation
so = SalesService.create_sales_order(
    customer_id=1,
    items=[...],
    payment_type='cash',
    created_by=user
)

# Process payment
so, receipt = SalesService.process_payment(
    sales_order_id=1,
    amount_paid=5000,
    created_by=user
)

# Get customer account summary
summary = SalesService.get_customer_account_summary(customer_id=1)
```

### OrderConfirmationService
```python
# Create confirmation
confirmation = OrderConfirmationService.create_order_confirmation(
    sales_order_id=1,
    estimated_pickup_date=date(2025, 12, 20),
    created_by=user
)

# Mark ready and notify
confirmation = OrderConfirmationService.confirm_order_ready(
    sales_order_id=1
)

# Mark payment complete
confirmation = OrderConfirmationService.mark_payment_received(
    sales_order_id=1
)

# Mark picked up
confirmation = OrderConfirmationService.mark_order_picked_up(
    sales_order_id=1
)

# Get customer pending pickups
pickups = OrderConfirmationService.get_customer_pending_pickups(
    customer_id=1
)

# Get customer notifications
notifications = OrderConfirmationService.get_customer_notifications(
    customer_id=1,
    unread_only=True,
    limit=20
)

# Mark notification as read
notif = OrderConfirmationService.mark_notification_read(notification_id=1)
```

---

## Admin Configuration

### OrderConfirmationAdmin Features
- **List Display**: SO Number, Customer, Status, Payment Status, Dates
- **Filters**: By status, payment status, creation date
- **Search**: By SO number, customer name, email
- **Actions**: Mark ready, mark payment, mark picked up
- **Fieldsets**: Organized by order info, pickup details, payment, timestamps

### OrderNotificationAdmin Features
- **List Display**: SO Number, Customer, Type, Read Status, Created Date
- **Filters**: By type, read status, creation date
- **Search**: By SO number, customer, title
- **Read-only**: Timestamp fields

---

## Database Queries

### Get all orders ready for pickup (not picked up)
```python
from app_sales.notification_models import OrderConfirmation

ready = OrderConfirmation.objects.filter(
    status='ready_for_pickup',
    customer__email='customer@example.com'
)
```

### Get orders with pending payment
```python
pending_payment = OrderConfirmation.objects.filter(
    status__in=['confirmed', 'ready_for_pickup'],
    is_payment_complete=False
)
```

### Get unread notifications for customer
```python
from app_sales.notification_models import OrderNotification

unread = OrderNotification.objects.filter(
    customer_id=1,
    is_read=False
).order_by('-created_at')
```

---

## Best Practices

1. **Always create OrderConfirmation** when creating sales order
2. **Set estimated_pickup_date** when confirming (default 3 days from creation)
3. **Mark payment complete** when payment is received
4. **Mark ready for pickup** in admin or via management command
5. **Use context processor** in templates for real-time notifications
6. **Monitor pending payments** to ensure timely follow-ups

---

## Testing

### Test order creation and notification
```python
from app_sales.services import SalesService
from app_sales.models import Customer
from app_sales.notification_models import OrderConfirmation, OrderNotification

# Create customer
customer = Customer.objects.create(
    name='John Doe',
    email='john@example.com',
    phone_number='09123456789'
)

# Create order
so = SalesService.create_sales_order(
    customer_id=customer.id,
    items=[{'product_id': 1, 'quantity_pieces': 10}],
    payment_type='cash'
)

# Check confirmation created
assert OrderConfirmation.objects.filter(sales_order=so).exists()

# Check notification sent
assert OrderNotification.objects.filter(
    sales_order=so,
    notification_type='order_confirmed'
).exists()

# Mark ready
confirmation = OrderConfirmation.objects.get(sales_order=so)
confirmation.mark_ready_for_pickup()

# Check ready notification sent
assert OrderNotification.objects.filter(
    sales_order=so,
    notification_type='ready_for_pickup'
).exists()
```

---

## Troubleshooting

### Notifications not appearing
1. Check if OrderNotification records exist in database
2. Verify context processor is enabled in settings.py
3. Ensure customer email matches authenticated user email
4. Check if notifications are marked as read

### Orders not showing as ready
1. Verify OrderConfirmation exists for the order
2. Check order status in admin
3. Ensure mark_ready_for_pickup() method was called
4. Check for validation errors in logs

### Payment status not updating
1. Verify is_payment_complete field is being set
2. Check if OrderConfirmation exists
3. Ensure mark_payment_complete() is called after payment

---

## Next Steps

1. Create customer dashboard template to display notifications
2. Add email notifications using Django signals
3. Implement SMS notifications via Twilio/similar service
4. Add notification preferences (email, SMS, app only)
5. Create notification history/archive view
6. Add batch operations for bulk order marking

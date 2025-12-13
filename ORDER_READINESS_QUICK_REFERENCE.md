# Order Readiness System - Quick Reference Card

## 🚀 How It Works in 30 Seconds

1. **Order Created** → Confirmation + Notification Auto-Created
2. **Admin Marks Ready** → Notification Sent to Customer  
3. **Customer Sees Alert** → Available in Dashboard & `/notifications/`
4. **Customer Picks Up** → Confirms in system

---

## 📍 Key URLs

| Page | URL | Purpose |
|------|-----|---------|
| Dashboard | `/dashboard/` | Main customer page (shows alerts) |
| Notifications | `/notifications/` | View all notification history |
| Ready Orders | `/ready-orders/` | See orders ready for pickup |
| Order Detail | `/orders/{id}/` | Full order info + confirmation |

---

## 🎯 Admin Actions (3 Ways)

### Way 1: Django Admin
```
1. Go to /admin/app_sales/orderconfirmation/
2. Check orders with status "Created"/"Confirmed"
3. Select action: "Mark selected orders as ready..."
4. Click Go ✓
```

### Way 2: Management Command
```bash
python manage.py mark_order_ready --all-pending
# Or specific:
python manage.py mark_order_ready --so-number="SO-20251213-0001"
```

### Way 3: API
```bash
curl -X POST http://localhost:8000/api/confirmations/1/mark_ready/ \
  -H "Authorization: Bearer TOKEN"
```

---

## 💾 Database Models

```
SalesOrder (existing)
├── customer
├── total_amount
├── payment_type
└── OrderConfirmation (new)
    ├── status: created→confirmed→ready→picked_up
    ├── is_payment_complete
    ├── estimated_pickup_date
    └── ready_at (timestamp)

OrderConfirmation
└── OrderNotification (multiple)
    ├── type: order_confirmed/ready_for_pickup/payment_completed
    ├── title
    ├── message
    └── is_read
```

---

## 🎨 Template Variables (Always Available)

```django
{{ notification_count }}          # Unread notification count
{{ notifications }}               # List of unread notifications
{{ ready_pickups_count }}        # Orders ready for pickup
{{ ready_pickups }}              # Ready orders with details
{{ payment_pending_count }}      # Orders awaiting payment
{{ has_ready_pickup_notifications }}  # True if order ready
{{ has_payment_notifications }}  # True if payment pending
```

---

## ✨ Features

| Feature | Status | How to Use |
|---------|--------|-----------|
| Auto-create confirmation | ✅ | Create order → auto happens |
| Auto-send notifications | ✅ | Mark ready → auto happens |
| Admin bulk actions | ✅ | `/admin/app_sales/orderconfirmation/` |
| Customer dashboard alerts | ✅ | `/dashboard/` shows all alerts |
| Notification history | ✅ | `/notifications/` page |
| Ready orders list | ✅ | `/ready-orders/` page |
| Payment status tracking | ✅ | Shows in all order views |
| Pickup confirmation | ✅ | Button in order detail |
| Context processor | ✅ | Auto in all templates |
| REST API | ✅ | `/api/confirmations/` & `/api/notifications/` |
| Management command | ✅ | `python manage.py mark_order_ready` |

---

## 🔄 Order Status Flow

```
CREATED
  ↓
CONFIRMED (optional)
  ↓
READY_FOR_PICKUP ← Notification sent here
  ↓
PICKED_UP
```

---

## 📢 Notification Types

| Type | Sent When | Message |
|------|-----------|---------|
| `order_confirmed` | Order created | "Order created successfully..." |
| `ready_for_pickup` | Admin marks ready | "Your order is ready for pickup!" |
| `payment_completed` | Payment received | "Payment received. Order ready!" |
| `payment_pending` | Order ready but unpaid | "Payment due: ₱5000" |

---

## 💡 Code Examples

### Check if customer has ready orders
```python
from app_sales.notification_models import OrderConfirmation

has_ready = OrderConfirmation.objects.filter(
    customer=customer,
    status='ready_for_pickup'
).exists()
```

### Get unread notifications
```python
from app_sales.notification_models import OrderNotification

unread = OrderNotification.objects.filter(
    customer=customer,
    is_read=False
)
```

### Mark order ready programmatically
```python
from app_sales.notification_models import OrderConfirmation

conf = OrderConfirmation.objects.get(sales_order_id=1)
conf.mark_ready_for_pickup()  # Notification auto-sent
```

### Mark payment received
```python
conf.mark_payment_complete()  # Notification auto-sent
```

---

## 🐛 Quick Debugging

**Check notifications exist:**
```bash
python manage.py dbshell
SELECT * FROM app_sales_ordernotification 
WHERE customer_id = 1;
```

**Check context processor working:**
```django
<!-- In any template -->
{{ notification_count }}
{{ ready_pickups }}
<!-- Should show data if customer has orders -->
```

**Check order confirmation exists:**
```bash
python manage.py dbshell
SELECT * FROM app_sales_orderconfirmation 
WHERE sales_order_id = 1;
```

---

## 📱 What Customer Sees

### On Dashboard (`/dashboard/`)
```
[✓ Your Orders Are Ready!]
You have 2 order(s) ready for pickup
[View Ready Orders]

[⚠️ Payment Due]
You have 1 order(s) awaiting payment
[Make Payment]

[🔔 New Notifications]
You have 3 new notification(s)
[View All Notifications]
```

### On Ready Orders (`/ready-orders/`)
```
Order #SO-20251213-0001
Total: ₱5000.00
Discount: -₱1000.00
Status: PAID ✓
Ready since: 2 days ago

[View Details] [Pickup Now]
```

### On Notifications (`/notifications/`)
```
📦 Your Order SO-20251213-0001 is Ready!
Good news! Your order is now ready for pickup...
Dec 13, 2024 at 10:30 AM
Order #SO-20251213-0001

[View Order]
```

---

## 🔐 Permissions

✅ Customer can:
- View their own notifications
- View their own ready orders
- Mark their own orders as picked up
- See payment status

❌ Customer cannot:
- View other customer's orders
- Mark other customer's orders ready
- Modify admin settings

✅ Admin can:
- Mark any order ready
- Mark any payment received
- Bulk manage orders
- Override any status

---

## 📊 Common Queries

### "How many orders are ready?"
```python
from app_sales.notification_models import OrderConfirmation
count = OrderConfirmation.objects.filter(
    status='ready_for_pickup'
).count()
```

### "Which customers have pending payments?"
```python
pending = OrderConfirmation.objects.filter(
    status__in=['confirmed', 'ready_for_pickup'],
    is_payment_complete=False
).values_list('customer', flat=True).distinct()
```

### "How long has order been ready?"
```python
from django.utils import timezone
from app_sales.notification_models import OrderConfirmation

conf = OrderConfirmation.objects.get(id=1)
days_ready = (timezone.now() - conf.ready_at).days
```

---

## ⚡ Performance Tips

- Context processor limits to 10-20 items (efficient)
- Uses `select_related()` for foreign keys
- Indexes on commonly filtered fields
- Pagination for large lists

---

## 🎓 Learning Path

1. **First**: Read `ORDER_READINESS_QUICK_START.md`
2. **Second**: Try marking order ready in admin
3. **Third**: View customer dashboard
4. **Fourth**: Check `/notifications/` page
5. **Fifth**: Read `ORDER_READINESS_NOTIFICATION_GUIDE.md` for details

---

## 🆘 "It's Not Working" Checklist

- [ ] Did you create an order? (If no, create one)
- [ ] Did you mark it ready? (Go to admin or use command)
- [ ] Is customer email matching? (Notifications require email match)
- [ ] Did you log in as customer? (Views require login)
- [ ] Did you check database? (Run `python manage.py dbshell`)
- [ ] Did you restart server? (Might need reload)

---

## 📞 Getting Help

**Documentation Files:**
- Quick start: `ORDER_READINESS_QUICK_START.md`
- Full guide: `ORDER_READINESS_NOTIFICATION_GUIDE.md`
- Implementation: `ORDER_READINESS_FINAL_IMPLEMENTATION.md`
- Examples: `ORDER_READINESS_TEMPLATES_EXAMPLES.md`
- Checklist: `ORDER_READINESS_IMPLEMENTATION_CHECKLIST.md`

**Code Comments:**
- Check `notification_views.py` for view logic
- Check `notification_models.py` for model details
- Check `services.py` for business logic

---

## 📈 What's Next?

### Easy Enhancements:
- [ ] Email notifications on order ready
- [ ] SMS notifications (Twilio)
- [ ] Notification preferences
- [ ] Order history/archive
- [ ] Rating/feedback system

### Medium Enhancements:
- [ ] Email templates
- [ ] Batch notifications
- [ ] Notification scheduling
- [ ] Analytics dashboard

### Advanced:
- [ ] Real-time updates (WebSocket)
- [ ] Mobile app integration
- [ ] Predictive notifications
- [ ] AI-based recommendations

---

**✅ System is ready to use. Go to `/dashboard/` as customer to see it in action!**

Last updated: December 13, 2025

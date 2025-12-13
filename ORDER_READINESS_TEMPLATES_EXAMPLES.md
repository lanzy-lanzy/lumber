# Order Readiness - HTML/Template Examples

Copy and paste these examples into your Django templates to display order notifications and ready orders.

---

## 1. Notification Bell (Navbar)

```html
<!-- Add to base.html navbar -->

<div class="navbar-right">
  <a href="/customer/notifications/" class="notification-bell position-relative" title="Notifications">
    <i class="bi bi-bell"></i>
    {% if notification_count > 0 %}
      <span class="badge badge-danger position-absolute top-0 start-100 translate-middle">
        {{ notification_count }}
      </span>
    {% endif %}
  </a>
</div>

<style>
  .notification-bell {
    position: relative;
    font-size: 1.5rem;
    color: #333;
    text-decoration: none;
    margin: 0 10px;
  }
  
  .notification-bell:hover {
    color: #007bff;
  }
  
  .notification-bell .badge {
    font-size: 0.7rem;
    padding: 0.25rem 0.4rem;
  }
</style>
```

---

## 2. Order Ready Alert (Dashboard Top)

```html
<!-- Add to customer dashboard -->

{% if has_ready_pickup_notifications %}
  <div class="alert alert-success alert-dismissible fade show" role="alert">
    <div class="d-flex align-items-center">
      <i class="bi bi-check-circle-fill me-2" style="font-size: 1.5rem;"></i>
      <div>
        <h4 class="alert-heading mb-2">📦 Your Order is Ready!</h4>
        <p class="mb-0">{{ ready_pickups_count }} order(s) ready for pickup</p>
      </div>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  </div>
{% endif %}

<style>
  .alert-success {
    border-left: 5px solid #28a745;
    background-color: #f0f9f6;
    border-color: #28a745;
  }
</style>
```

---

## 3. Ready Orders Cards

```html
<!-- Display all orders ready for pickup -->

{% if ready_pickups %}
  <div class="ready-orders-section mt-4">
    <h5 class="mb-3">
      <i class="bi bi-box-seam"></i> Ready for Pickup
    </h5>
    
    <div class="row">
      {% for pickup in ready_pickups %}
        <div class="col-md-6 col-lg-4 mb-3">
          <div class="card border-success h-100">
            <div class="card-header bg-success text-white">
              <h6 class="mb-0">Order #{{ pickup.order_number }}</h6>
            </div>
            
            <div class="card-body">
              <dl class="row mb-0">
                <dt class="col-sm-6">Amount:</dt>
                <dd class="col-sm-6 text-end">₱{{ pickup.total_amount|floatformat:2 }}</dd>
                
                <dt class="col-sm-6">Discount:</dt>
                <dd class="col-sm-6 text-end">{{ pickup.discount_amount|floatformat:2 }}</dd>
                
                <dt class="col-sm-6">Payment:</dt>
                <dd class="col-sm-6">
                  {% if pickup.payment_complete %}
                    <span class="badge bg-success">PAID</span>
                  {% else %}
                    <span class="badge bg-warning">DUE: ₱{{ pickup.balance|floatformat:2 }}</span>
                  {% endif %}
                </dd>
                
                <dt class="col-sm-6">Ready Since:</dt>
                <dd class="col-sm-6 text-end">
                  {% if pickup.days_ready == 0 %}
                    <span class="badge bg-info">Today</span>
                  {% elif pickup.days_ready == 1 %}
                    <span class="badge bg-info">Yesterday</span>
                  {% else %}
                    <span class="badge">{{ pickup.days_ready }} days ago</span>
                  {% endif %}
                </dd>
              </dl>
            </div>
            
            <div class="card-footer bg-light">
              <a href="/orders/{{ pickup.id }}/" class="btn btn-sm btn-primary">
                View Details
              </a>
              <a href="/orders/{{ pickup.id }}/pickup/" class="btn btn-sm btn-success">
                Pickup Order
              </a>
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
{% endif %}

<style>
  .ready-orders-section {
    margin-top: 2rem;
  }
  
  .card {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    transition: transform 0.2s;
  }
  
  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  }
  
  .card-header {
    padding: 1rem;
  }
  
  .card-footer {
    display: flex;
    gap: 0.5rem;
  }
  
  .card-footer .btn {
    flex: 1;
  }
</style>
```

---

## 4. Payment Due Alert

```html
<!-- Show orders with pending payment -->

{% if has_payment_notifications %}
  <div class="alert alert-warning alert-dismissible fade show mt-3" role="alert">
    <div class="d-flex align-items-center">
      <i class="bi bi-exclamation-triangle-fill me-2" style="font-size: 1.5rem;"></i>
      <div>
        <h5 class="alert-heading mb-2">⚠️ Payment Due</h5>
        <p class="mb-0">{{ payment_pending_count }} order(s) awaiting payment</p>
      </div>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  </div>
{% endif %}

{% if payment_pending_orders %}
  <div class="payment-due-section mt-3">
    <h5 class="mb-3">Orders Awaiting Payment</h5>
    
    <table class="table table-hover">
      <thead class="table-light">
        <tr>
          <th>Order #</th>
          <th>Total</th>
          <th>Balance Due</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {% for order in payment_pending_orders %}
          <tr>
            <td><strong>{{ order.order_number }}</strong></td>
            <td>₱{{ order.total_amount|floatformat:2 }}</td>
            <td>
              <span class="badge bg-danger">₱{{ order.balance_due|floatformat:2 }}</span>
            </td>
            <td>{{ order.status }}</td>
            <td>
              <a href="/orders/{{ order.id }}/pay/" class="btn btn-sm btn-primary">
                Pay Now
              </a>
            </td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
{% endif %}

<style>
  .table-hover tbody tr:hover {
    background-color: #f5f5f5;
  }
  
  .table tbody td {
    vertical-align: middle;
  }
</style>
```

---

## 5. Notifications Dropdown

```html
<!-- Notification dropdown for navbar -->

<div class="dropdown">
  <button 
    class="btn btn-outline-secondary dropdown-toggle position-relative" 
    type="button" 
    id="notificationDropdown"
    data-bs-toggle="dropdown" 
    aria-expanded="false">
    <i class="bi bi-bell"></i>
    {% if notification_count > 0 %}
      <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
        {{ notification_count }}
      </span>
    {% endif %}
  </button>
  
  <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="notificationDropdown" style="width: 350px;">
    {% if notifications %}
      {% for notif in notifications %}
        <li>
          <a class="dropdown-item" href="#" data-notif-id="{{ notif.id }}">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <h6 class="mb-1">{{ notif.title }}</h6>
                <p class="mb-1 small text-muted">{{ notif.message|truncatewords:15 }}</p>
                <small class="text-muted">{{ notif.created_at|date:"M d, Y H:i" }}</small>
              </div>
              {% if not notif.is_read %}
                <span class="badge bg-primary">New</span>
              {% endif %}
            </div>
          </a>
        </li>
        <li><hr class="dropdown-divider"></li>
      {% endfor %}
      
      <li>
        <a class="dropdown-item text-center small" href="/customer/notifications/">
          View All Notifications
        </a>
      </li>
    {% else %}
      <li>
        <p class="text-center py-3 text-muted">
          No new notifications
        </p>
      </li>
    {% endif %}
  </ul>
</div>

<style>
  .dropdown-item {
    border-bottom: 1px solid #eee;
    cursor: pointer;
  }
  
  .dropdown-item:hover {
    background-color: #f8f9fa;
  }
  
  .dropdown-menu h6 {
    color: #333;
    font-weight: 600;
  }
</style>
```

---

## 6. Full Customer Dashboard Example

```html
<!-- customer/dashboard.html -->

{% extends 'base.html' %}

{% block title %}Customer Dashboard{% endblock %}

{% block content %}
<div class="container py-4">
  <!-- Welcome Section -->
  <div class="row mb-4">
    <div class="col-md-8">
      <h2>Welcome, {{ request.user.first_name }}!</h2>
      <p class="text-muted">Here's your order status and notifications</p>
    </div>
    <div class="col-md-4 text-md-end">
      <a href="/orders/" class="btn btn-primary">View All Orders</a>
    </div>
  </div>
  
  <!-- Alerts Section -->
  {% if has_ready_pickup_notifications or has_payment_notifications %}
    <div class="alerts-section mb-4">
      <!-- Ready for Pickup Alert -->
      {% if has_ready_pickup_notifications %}
        <div class="alert alert-success alert-dismissible fade show" role="alert">
          <div class="d-flex align-items-center">
            <i class="bi bi-check-circle-fill me-2" style="font-size: 1.5rem;"></i>
            <div>
              <h5 class="alert-heading mb-1">📦 Your Order is Ready!</h5>
              <p class="mb-0">
                {{ ready_pickups_count }} order(s) ready for pickup. 
                Come visit our store!
              </p>
            </div>
          </div>
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
      {% endif %}
      
      <!-- Payment Due Alert -->
      {% if has_payment_notifications %}
        <div class="alert alert-warning alert-dismissible fade show" role="alert">
          <div class="d-flex align-items-center">
            <i class="bi bi-exclamation-triangle-fill me-2" style="font-size: 1.5rem;"></i>
            <div>
              <h5 class="alert-heading mb-1">⚠️ Payment Due</h5>
              <p class="mb-0">
                {{ payment_pending_count }} order(s) awaiting payment. 
                Please complete payment to complete pickup.
              </p>
            </div>
          </div>
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
      {% endif %}
    </div>
  {% endif %}
  
  <!-- Ready Pickup Orders -->
  {% if ready_pickups %}
    <div class="section mb-4">
      <h4 class="mb-3">
        <i class="bi bi-box-seam"></i> Orders Ready for Pickup
        <span class="badge bg-success">{{ ready_pickups_count }}</span>
      </h4>
      
      <div class="row">
        {% for pickup in ready_pickups %}
          <div class="col-md-6 col-lg-4 mb-3">
            <div class="card border-success">
              <div class="card-header bg-success text-white">
                <h6 class="mb-0">{{ pickup.order_number }}</h6>
              </div>
              <div class="card-body">
                <dl class="row small mb-2">
                  <dt class="col-6">Amount:</dt>
                  <dd class="col-6 text-end">₱{{ pickup.total_amount|floatformat:2 }}</dd>
                  
                  <dt class="col-6">Payment:</dt>
                  <dd class="col-6 text-end">
                    {% if pickup.payment_complete %}
                      <span class="badge bg-success">PAID</span>
                    {% else %}
                      <span class="badge bg-warning">DUE: ₱{{ pickup.balance|floatformat:2 }}</span>
                    {% endif %}
                  </dd>
                  
                  <dt class="col-6">Ready:</dt>
                  <dd class="col-6 text-end">{{ pickup.days_ready }} days ago</dd>
                </dl>
              </div>
              <div class="card-footer d-grid gap-2">
                <a href="/orders/{{ pickup.id }}/pickup/" class="btn btn-sm btn-success">
                  Pickup Now
                </a>
              </div>
            </div>
          </div>
        {% endfor %}
      </div>
    </div>
  {% endif %}
  
  <!-- Payment Due Orders -->
  {% if payment_pending_orders %}
    <div class="section mb-4">
      <h4 class="mb-3">
        <i class="bi bi-credit-card"></i> Payment Due
        <span class="badge bg-warning">{{ payment_pending_count }}</span>
      </h4>
      
      <div class="table-responsive">
        <table class="table table-hover">
          <thead class="table-light">
            <tr>
              <th>Order #</th>
              <th>Amount</th>
              <th>Balance</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {% for order in payment_pending_orders %}
              <tr>
                <td><strong>{{ order.order_number }}</strong></td>
                <td>₱{{ order.total_amount|floatformat:2 }}</td>
                <td>
                  <span class="badge bg-danger">
                    ₱{{ order.balance_due|floatformat:2 }}
                  </span>
                </td>
                <td>{{ order.status }}</td>
                <td>
                  <a href="/orders/{{ order.id }}/pay/" class="btn btn-sm btn-primary">
                    Pay
                  </a>
                </td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  {% endif %}
  
  <!-- Recent Notifications -->
  {% if notifications %}
    <div class="section">
      <h4 class="mb-3">
        <i class="bi bi-bell"></i> Recent Notifications
        {% if notification_count > 0 %}
          <span class="badge bg-primary">{{ notification_count }}</span>
        {% endif %}
      </h4>
      
      <div class="list-group">
        {% for notif in notifications %}
          <a href="#" class="list-group-item list-group-item-action">
            <div class="d-flex w-100 justify-content-between align-items-start">
              <div>
                <h6 class="mb-1">{{ notif.title }}</h6>
                <p class="mb-1 text-muted small">{{ notif.message }}</p>
                <small class="text-muted">{{ notif.created_at|date:"M d, Y H:i" }}</small>
              </div>
              {% if not notif.is_read %}
                <span class="badge bg-primary ms-2">New</span>
              {% endif %}
            </div>
          </a>
        {% endfor %}
      </div>
      
      {% if notification_count > 5 %}
        <div class="mt-3">
          <a href="/customer/notifications/" class="btn btn-outline-secondary btn-sm">
            View All Notifications
          </a>
        </div>
      {% endif %}
    </div>
  {% endif %}
</div>

<style>
  .section {
    background: white;
    padding: 1.5rem;
    border-radius: 0.5rem;
    border: 1px solid #eee;
  }
  
  .card {
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .card:hover {
    transform: translateY(-3px);
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  }
  
  .alert {
    margin-bottom: 1rem;
  }
</style>
{% endblock %}
```

---

## 7. Notification History Page

```html
<!-- customer/notifications.html -->

{% extends 'base.html' %}

{% block title %}Notifications{% endblock %}

{% block content %}
<div class="container py-4">
  <div class="row mb-4">
    <div class="col-md-8">
      <h2>Notifications</h2>
      <p class="text-muted">{{ notification_count }} unread notification(s)</p>
    </div>
    <div class="col-md-4 text-md-end">
      {% if notification_count > 0 %}
        <form method="post" action="/notifications/mark-all-read/" class="d-inline">
          {% csrf_token %}
          <button type="submit" class="btn btn-outline-secondary btn-sm">
            Mark All as Read
          </button>
        </form>
      {% endif %}
    </div>
  </div>
  
  {% if notifications %}
    <div class="list-group">
      {% for notif in notifications %}
        <div class="list-group-item {% if not notif.is_read %}bg-light border-primary border-3{% endif %}">
          <div class="d-flex justify-content-between align-items-start">
            <div class="flex-grow-1">
              <h5 class="mb-2">{{ notif.title }}</h5>
              <p class="mb-2">{{ notif.message }}</p>
              <small class="text-muted">
                <i class="bi bi-calendar"></i> {{ notif.created_at|date:"F d, Y \a\t H:i" }}
                {% if notif.order_number %}
                  | <strong>Order #{{ notif.order_number }}</strong>
                {% endif %}
              </small>
            </div>
            <span class="badge bg-{{ notif.type|badge_color }}">{{ notif.type|format_type }}</span>
          </div>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <div class="alert alert-info text-center py-5">
      <i class="bi bi-bell-slash" style="font-size: 3rem;"></i>
      <p class="mt-3 mb-0">No notifications yet</p>
    </div>
  {% endif %}
</div>
{% endblock %}
```

---

## CSS Classes Reference

```css
/* Notification statuses */
.notification-ready-for-pickup   /* Green - Order ready */
.notification-payment-completed  /* Blue - Payment received */
.notification-payment-pending    /* Orange - Payment due */
.notification-order-confirmed    /* Light blue - Order created */

/* Badge colors */
.badge.bg-success    /* Green - PAID */
.badge.bg-warning    /* Orange - DUE */
.badge.bg-danger     /* Red - Amount due */
.badge.bg-info       /* Light blue - Time info */
.badge.bg-primary    /* Blue - New items */

/* Card status indicators */
.border-success      /* Green border - Ready orders */
.card-header.bg-success  /* Green header - Ready status */
```

---

## Bootstrap Icons Used

```
bi-bell               - Notification bell
bi-bell-slash        - No notifications
bi-box-seam          - Package/order
bi-check-circle-fill - Checkmark (ready)
bi-exclamation-triangle-fill - Warning (payment)
bi-credit-card       - Payment/billing
bi-calendar          - Date/time
```

---

**Ready to use!** Copy these snippets into your templates and customize colors/styling as needed.

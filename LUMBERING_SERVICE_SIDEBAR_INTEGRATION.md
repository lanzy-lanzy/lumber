# Lumbering Service - Sidebar Integration Guide

## Overview

The Lumbering Service system is fully integrated into the admin sidebar and is accessible via:

1. **Web Dashboard** - `/lumbering/`
2. **Django Admin** - `/admin/app_lumbering_service/`
3. **REST API** - `/api/lumbering-service-*`

## Sidebar Menu Structure

Add this to your main navigation/sidebar template:

```html
<li class="nav-item">
    <a class="nav-link" href="{% url 'lumbering_service:dashboard' %}">
        <i class="fas fa-wood"></i>
        <span>Lumbering Service</span>
    </a>
    <ul class="submenu" style="display: none;">
        <li><a href="{% url 'lumbering_service:dashboard' %}">Dashboard</a></li>
        <li><a href="{% url 'lumbering_service:order_list' %}">Service Orders</a></li>
        <li><a href="{% url 'lumbering_service:order_create' %}">New Order</a></li>
    </ul>
</li>
```

## URL Routes Reference

### Dashboard & List Views
- **Dashboard:** `/lumbering/` (name: `lumbering_service:dashboard`)
- **Order List:** `/lumbering/orders/` (name: `lumbering_service:order_list`)

### Order Management
- **Create Order:** `/lumbering/orders/create/` (name: `lumbering_service:order_create`)
- **View Order:** `/lumbering/orders/<id>/` (name: `lumbering_service:order_detail`)

### Lumber Output
- **Add Output:** `/lumbering/orders/<id>/outputs/create/` (name: `lumbering_service:output_create`)

### Shavings Management
- **Record Shavings:** `/lumbering/orders/<id>/shavings/create/` (name: `lumbering_service:shavings_create`)

### Django Admin
- **Admin Root:** `/admin/` → Lumbering Service section
- **Orders:** `/admin/app_lumbering_service/lumberingserviceorder/`
- **Outputs:** `/admin/app_lumbering_service/lumberingserviceoutput/`
- **Shavings:** `/admin/app_lumbering_service/shavingsrecord/`

## Integration Points

### Existing User Model
Uses `core.models.CustomUser` for tracking who created orders:
- Created by user is auto-captured when order is created
- Visible in admin and order history

### Existing Customer Model
Integrates with `app_sales.models.Customer`:
- All service orders reference existing customers
- Customer dropdown in order creation form
- Customer name displayed throughout

### Existing Database
- Uses your existing SQLite database
- Migrations already applied
- No external dependencies

## Sidebar Template Integration Examples

### Bootstrap Navbar Example
```html
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="lumberingNav" role="button" data-bs-toggle="dropdown">
        <i class="fas fa-wood"></i> Lumbering Service
    </a>
    <ul class="dropdown-menu" aria-labelledby="lumberingNav">
        <li><a class="dropdown-item" href="{% url 'lumbering_service:dashboard' %}">Dashboard</a></li>
        <li><a class="dropdown-item" href="{% url 'lumbering_service:order_list' %}">Service Orders</a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="{% url 'lumbering_service:order_create' %}">New Service Order</a></li>
    </ul>
</li>
```

### Simple List Example
```html
<li>
    <a href="{% url 'lumbering_service:dashboard' %}">Lumbering Service</a>
    <ul>
        <li><a href="{% url 'lumbering_service:order_list' %}">Orders</a></li>
        <li><a href="{% url 'lumbering_service:order_create' %}">New Order</a></li>
    </ul>
</li>
```

## Permissions & Access Control

Currently no role-based restrictions. To add admin-only access:

```python
# Add to any view:
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def lumbering_dashboard(request):
    # View only accessible to admins
    ...
```

Or restrict at the URL level in `urls.py`:

```python
from django.contrib.auth.decorators import user_passes_test

urlpatterns = [
    path('', user_passes_test(lambda u: u.is_staff)(views.lumbering_dashboard), name='dashboard'),
    ...
]
```

## Database Statistics

The sidebar might want to display quick stats. Use these queries:

```python
from app_lumbering_service.models import LumberingServiceOrder
from django.db.models import Sum

# Total orders
total = LumberingServiceOrder.objects.count()

# Pending orders
pending = LumberingServiceOrder.objects.filter(status='pending').count()

# Total service fees
total_fees = LumberingServiceOrder.objects.aggregate(
    Sum('total_service_fee')
)['total_service_fee__sum'] or 0

# Total board feet
from app_lumbering_service.models import LumberingServiceOutput
total_bf = LumberingServiceOutput.objects.aggregate(
    Sum('board_feet')
)['board_feet__sum'] or 0
```

## Dashboard Card Examples

### Quick Stats Card
```html
<div class="card">
    <div class="card-body">
        <h6>Lumbering Service</h6>
        <p>{{ pending_orders }} pending | {{ total_orders }} total</p>
        <a href="{% url 'lumbering_service:dashboard' %}">View Dashboard</a>
    </div>
</div>
```

### Recent Orders Card
```html
<div class="card">
    <div class="card-header">Recent Service Orders</div>
    <ul class="list-group">
        {% for order in recent_orders %}
        <li class="list-group-item">
            <a href="{% url 'lumbering_service:order_detail' order.id %}">
                #{{ order.id }} - {{ order.customer.name }}
            </a>
        </li>
        {% endfor %}
    </ul>
</div>
```

## Navigation Context Example

To pass lumbering stats to all templates via context processor:

Create `app_lumbering_service/context_processors.py`:

```python
from app_lumbering_service.models import LumberingServiceOrder
from django.db.models import Sum

def lumbering_context(request):
    """Add lumbering service stats to template context"""
    orders = LumberingServiceOrder.objects.all()
    
    return {
        'lumbering_stats': {
            'total_orders': orders.count(),
            'pending_orders': orders.filter(status='pending').count(),
            'completed_orders': orders.filter(status='completed').count(),
            'total_fees': orders.aggregate(Sum('total_service_fee'))['total_service_fee__sum'] or 0,
        }
    }
```

Then add to `settings.py`:

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... existing processors
                'app_lumbering_service.context_processors.lumbering_context',
            ],
        },
    },
]
```

Then use in templates:

```html
<a href="{% url 'lumbering_service:dashboard' %}">
    Service Orders ({{ lumbering_stats.pending_orders }} pending)
</a>
```

## Mobile Responsive Example

For mobile-friendly sidebar:

```html
<li class="nav-item">
    <a class="nav-link" href="{% url 'lumbering_service:dashboard' %}" 
       data-bs-toggle="collapse" data-bs-target="#lumberingMenu"
       aria-expanded="false" aria-controls="lumberingMenu">
        <i class="fas fa-wood"></i>
        <span class="d-none d-md-inline">Lumbering Service</span>
    </a>
    <div class="collapse" id="lumberingMenu">
        <ul class="list-unstyled ps-4">
            <li><a href="{% url 'lumbering_service:order_list' %}">Orders</a></li>
            <li><a href="{% url 'lumbering_service:order_create' %}">New Order</a></li>
        </ul>
    </div>
</li>
```

## Feature Checklist

✅ Models defined and migrated  
✅ Admin interface configured  
✅ Web dashboard created  
✅ REST API endpoints registered  
✅ URL routing configured  
✅ Templates created  
✅ Automatic calculations working  
✅ Database migrations applied  
✅ Ready for sidebar integration  

## Next Steps

1. **Add to sidebar:** Include the lumbering service links in your main navigation template
2. **Add stats:** Use context processor to show quick stats
3. **Test workflows:** Create test orders and verify calculations
4. **Customize fees:** Adjust default service fee per BF as needed
5. **Configure permissions:** Add role-based access if desired
6. **Add to dashboard:** Include lumbering cards on main dashboard

## Support

- **Full Documentation:** `LUMBERING_SERVICE_IMPLEMENTATION.md`
- **Quick Start:** `LUMBERING_SERVICE_QUICK_START.md`
- **Django Admin:** `/admin/app_lumbering_service/`
- **API Root:** `/api/`

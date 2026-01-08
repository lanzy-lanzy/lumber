# Fix: NoReverseMatch for 'purchase-orders' URL

## Problem
The application was throwing a `NoReverseMatch` error when accessing the dashboard:
```
Reverse for 'purchase-orders' not found. 'purchase-orders' is not a valid view function or pattern name.
```

## Root Cause
The dashboard template (`admin_dashboard.html`) referenced a URL named `'purchase-orders'`, but:
1. The URL pattern was defined in the comments in `templates/urls_frontend.py` (documentation only)
2. The view function `purchase_orders()` was missing from `core/frontend_views.py`
3. The import and URL pattern were missing from `core/urls.py`

## Solution

### 1. Added Missing View Function
**File**: `core/frontend_views.py`
```python
@login_required
@role_required('admin', 'inventory_manager')
def purchase_orders(request):
    """Purchase Orders management"""
    context = {
        'page_title': 'Purchase Orders',
        'breadcrumbs': ['Supplier', 'POs'],
    }
    return render(request, 'supplier/purchase_orders.html', context)
```

### 2. Updated URL Imports
**File**: `core/urls.py`
```python
from .frontend_views import (
    categories, products, stock_in, stock_out, stock_adjustment,
    pos, sales_orders,
    delivery_queue, deliveries, all_pickups,
    suppliers, purchase_orders,  # Added this
    inventory_reports, sales_reports
)
```

### 3. Added URL Pattern
**File**: `core/urls.py`
```python
# Supplier Routes
path('supplier/suppliers/', suppliers, name='suppliers'),
path('supplier/purchase-orders/', purchase_orders, name='purchase-orders'),  # Added this
```

### 4. Added Missing Views to core/views.py
Also added all missing frontend views to `core/views.py` as a backup:
- `products()`
- `inventory_dashboard()`
- `stock_in()`
- `stock_out()`
- `stock_adjustment()`
- `pos()`
- `sales_orders()`
- `delivery_queue()`
- `deliveries()`
- `suppliers()`
- `purchase_orders()`
- `inventory_reports()`
- `sales_reports()`
- `delivery_reports()`

## Testing
✅ Django system check passes
✅ No syntax errors
✅ URL pattern properly registered

## How to Verify
1. Start the server: `python manage.py runserver`
2. Navigate to `/dashboard/`
3. Click on "Purchase Orders" card
4. Should navigate to `/supplier/purchase-orders/` without errors

## Files Modified
- `core/views.py` - Added view functions with role decorators
- `core/frontend_views.py` - Added `purchase_orders()` view
- `core/urls.py` - Added import and URL pattern for purchase_orders

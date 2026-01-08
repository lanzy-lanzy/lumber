# Simplified Round Wood System - Migration Guide

## Overview
This guide walks you through replacing the complex round wood system with a simple one.

---

## Step 1: Backup Current System

```bash
# Backup database
cp db.sqlite3 db.sqlite3.backup

# Backup current models
cp app_round_wood/models.py app_round_wood/models_complex_backup.py
cp app_round_wood/serializers.py app_round_wood/serializers_complex_backup.py
cp app_round_wood/views.py app_round_wood/views_complex_backup.py
```

---

## Step 2: Replace Model Files

```bash
# Replace models.py with simplified version
cp app_round_wood/models_simplified.py app_round_wood/models.py

# Replace serializers.py with simplified version
cp app_round_wood/serializers_simplified.py app_round_wood/serializers.py

# Replace views.py with simplified version
cp app_round_wood/views_simplified.py app_round_wood/views.py
```

---

## Step 3: Create and Run Migration

```bash
# Create migration for model changes
python manage.py makemigrations app_round_wood

# Review the migration file to ensure it:
# - Removes: expected_delivery_date, inspection_date, inspection_status, 
#   inspection_notes, inspector_name, quantity_accepted, quantity_rejected,
#   quality_grade, ownership_transfer_status, approved_by, RoundWoodProcurementLog
# - Adds: payment_status field
# - Keeps: Everything else, RoundWoodInventory

# Apply migration
python manage.py migrate app_round_wood
```

---

## Step 4: Update URLs

If your `urls.py` references complex views/actions, update to use simplified routes:

```python
# urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    WoodTypeViewSet,
    RoundWoodPurchaseOrderViewSet,
    RoundWoodPurchaseOrderItemViewSet,
    RoundWoodInventoryViewSet
)

router = DefaultRouter()
router.register(r'wood-types', WoodTypeViewSet, basename='woodtype')
router.register(r'round-wood-purchases', RoundWoodPurchaseOrderViewSet, basename='rwpo')
router.register(r'round-wood-items', RoundWoodPurchaseOrderItemViewSet, basename='rwpo-item')
router.register(r'round-wood-inventory', RoundWoodInventoryViewSet, basename='rw-inventory')

urlpatterns = router.urls
```

---

## Step 5: Update Admin (Optional)

Create simplified admin.py:

```python
from django.contrib import admin
from .models import (
    WoodType,
    RoundWoodPurchaseOrder,
    RoundWoodPurchaseOrderItem,
    RoundWoodInventory
)


@admin.register(WoodType)
class WoodTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'is_active']
    list_filter = ['species', 'is_active']
    search_fields = ['name', 'description']


class RoundWoodPurchaseOrderItemInline(admin.TabularInline):
    model = RoundWoodPurchaseOrderItem
    fields = ['wood_type', 'quantity_logs', 'diameter_inches', 'length_feet',
              'volume_cubic_feet', 'unit_cost_per_cubic_foot', 'subtotal']
    read_only_fields = ['volume_cubic_feet', 'subtotal']
    extra = 1


@admin.register(RoundWoodPurchaseOrder)
class RoundWoodPurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'supplier', 'status', 'payment_status',
                    'order_date', 'delivery_date', 'total_amount']
    list_filter = ['status', 'payment_status', 'order_date', 'supplier']
    search_fields = ['po_number', 'po_number_supplier', 'supplier__company_name']
    readonly_fields = ['po_number', 'created_at', 'updated_at']
    inlines = [RoundWoodPurchaseOrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('po_number', 'po_number_supplier', 'supplier')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Dates', {
            'fields': ('order_date', 'delivery_date')
        }),
        ('Financial', {
            'fields': ('total_volume_cubic_feet', 'unit_cost_per_cubic_foot', 'total_amount')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Audit', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RoundWoodInventory)
class RoundWoodInventoryAdmin(admin.ModelAdmin):
    list_display = ['wood_type', 'total_logs_in_stock', 'total_cubic_feet_in_stock',
                    'average_cost_per_cubic_foot', 'warehouse_location']
    list_filter = ['wood_type', 'last_stock_in_date']
    search_fields = ['wood_type__name', 'warehouse_location']
    readonly_fields = ['total_logs_in_stock', 'total_cubic_feet_in_stock',
                       'total_cost_invested', 'average_cost_per_cubic_foot',
                       'last_stock_in_date', 'last_updated']
```

---

## Step 6: Test the System

### Test via API

```bash
# 1. Create order
curl -X POST http://localhost:8000/api/round-wood-purchases/ \
  -H "Content-Type: application/json" \
  -d '{
    "supplier": 1,
    "unit_cost_per_cubic_foot": 50.00,
    "order_date": "2025-12-15"
  }'

# 2. Add items
curl -X POST http://localhost:8000/api/round-wood-items/ \
  -H "Content-Type: application/json" \
  -d '{
    "purchase_order": 1,
    "wood_type": 1,
    "quantity_logs": 100,
    "diameter_inches": 12.0,
    "length_feet": 16.0,
    "unit_cost_per_cubic_foot": 50.00
  }'

# 3. Mark as ordered
curl -X POST http://localhost:8000/api/round-wood-purchases/1/order/

# 4. Mark as delivered
curl -X POST http://localhost:8000/api/round-wood-purchases/1/deliver/ \
  -H "Content-Type: application/json" \
  -d '{"delivery_date": "2025-12-20"}'

# 5. Mark as paid
curl -X POST http://localhost:8000/api/round-wood-purchases/1/pay/

# 6. Check inventory (should be updated)
curl http://localhost:8000/api/round-wood-inventory/
```

### Test Admin Interface

1. Go to Django admin: http://localhost:8000/admin/
2. Create a new order manually
3. Add items
4. Test status buttons
5. Verify inventory updates

---

## Step 7: Delete Old Models (If Migrating Data)

If you need to migrate existing data from complex system:

```python
# Create a data migration first

# Get data from old tables:
# - RoundWoodPurchaseOrder (old)
# - Extract needed fields
# - Create new simplified orders

# Skip these old models:
# - RoundWoodStockTransaction (no longer needed - auto-updated on deliver)
# - RoundWoodProcurementLog (no longer needed - timestamps on models)
```

---

## Step 8: Update Frontend (If Using)

### Simplified Workflow Buttons

```html
<!-- Draft order -->
<button onclick="markAsOrdered()">Order Now</button>

<!-- Ordered -->
<button onclick="openDeliveryDialog()">Mark Delivered</button>
<input type="date" id="deliveryDate" />

<!-- Delivered (unpaid) -->
<button onclick="markAsPaid()">Pay Supplier</button>

<!-- Delivered (paid) = Complete -->
<span class="badge badge-success">Complete</span>
```

### Status Display

```html
<!-- Simple status badge -->
<span class="badge" [class.bg-secondary]="order.status === 'draft'"
                    [class.bg-info]="order.status === 'ordered'"
                    [class.bg-success]="order.status === 'delivered'">
  {{ order.status | titlecase }}
</span>

<!-- Payment status -->
<span class="badge" [class.bg-warning]="!order.payment_status"
                    [class.bg-success]="order.payment_status === 'paid'">
  {{ order.payment_status | titlecase }}
</span>
```

---

## Step 9: Documentation Updates

Update these docs if they exist:

- ❌ Remove: ROUND_WOOD_SYSTEM_OVERVIEW.md
- ❌ Remove: ROUND_WOOD_PURCHASING_IMPLEMENTATION.md
- ✅ Keep: SIMPLIFIED_ROUND_WOOD_SYSTEM.md (this approach)
- ✅ Create: SIMPLE_QUICK_START.md

---

## Rollback (If Needed)

```bash
# Restore from backup
cp db.sqlite3.backup db.sqlite3

# Restore old code
cp app_round_wood/models_complex_backup.py app_round_wood/models.py
cp app_round_wood/serializers_complex_backup.py app_round_wood/serializers.py
cp app_round_wood/views_complex_backup.py app_round_wood/views.py

# Revert migration
python manage.py migrate app_round_wood [previous_migration_number]
```

---

## What Changes for Users

### Old Workflow (Complex)
```
Draft → Submitted → Confirmed → In Transit → Delivered → 
Inspected (pass/fail) → Stocked → Paid
(8+ steps, multiple statuses, inspection required)
```

### New Workflow (Simple)
```
Draft → Ordered → Delivered → Paid
(4 steps, simple status, no inspection)
```

### Key Differences

| Aspect | Old | New |
|--------|-----|-----|
| **Inspection** | Mandatory | ❌ Removed |
| **Delivery Date** | Expected + Actual | ✅ Only actual |
| **Quality Grades** | Tracked per item | ❌ Removed |
| **Ownership Transfer** | 3-stage tracking | ❌ Removed |
| **Stock-in** | Manual after inspection | ✅ Auto on delivery |
| **Payment** | Tracked separately | ✅ Simple unpaid/paid flag |
| **Statuses** | 8 options | ✅ 4 options |
| **Time to Complete** | 7-14 days | ✅ Same day possible |

---

## Testing Checklist

- [ ] Create draft order
- [ ] Add items with automatic volume calculation
- [ ] Mark as ordered
- [ ] Mark as delivered with date
- [ ] Verify inventory updated
- [ ] Mark as paid
- [ ] Check payment_status changed
- [ ] View list of unpaid orders
- [ ] Cancel a draft order
- [ ] Admin interface works
- [ ] API endpoints functional
- [ ] Summary statistics show correct totals

---

## Performance Notes

### Improved
- ✅ No inspection workflow = faster processing
- ✅ Fewer database records (no logs/transactions tables)
- ✅ Direct inventory update = no manual stock-in step
- ✅ Simpler queries = faster list views

### Same
- Database size reduced (fewer models)
- All needed data still tracked

---

## Post-Migration Support

For questions about:
- **API usage**: See SIMPLIFIED_ROUND_WOOD_SYSTEM.md
- **Workflow**: See the 4-step process above
- **Data**: Old backup preserved in db.sqlite3.backup
- **Admin**: Use Django admin interface directly

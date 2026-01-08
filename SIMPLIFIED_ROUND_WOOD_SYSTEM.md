# Simplified Round Wood Purchasing System

## Overview
**Goal**: Simple record-only purchase orders with payment on delivery date.
- No inspections
- No expected delivery date (only actual)
- No ownership transfer tracking
- No quality grades
- Minimal status tracking (just: Draft → Ordered → Delivered)

---

## New Simplified Models

### 1. WoodType (Unchanged)
```python
- name (unique)
- species (hardwood, softwood, etc.)
- description
- is_active
- timestamps
```

### 2. RoundWoodPurchaseOrder (Simplified)
```python
STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('ordered', 'Ordered'),           # Submitted to supplier
    ('delivered', 'Delivered'),       # Received & paid
    ('cancelled', 'Cancelled'),
]

Fields:
- po_number (auto-generated: RWPO-YYYY-####)
- supplier (FK)
- status (default: 'draft')
- order_date (auto: today)
- delivery_date (when goods arrive)  # ONLY actual date, no expected
- total_volume_cubic_feet
- unit_cost_per_cubic_foot
- total_amount (auto-calculated)
- payment_status (choices: unpaid, paid)  # Track if paid
- notes
- created_by (FK to User)
- created_at
- updated_at

Methods:
- calculate_total() - total_amount = total_volume × unit_cost
- mark_as_delivered(delivery_date, paid=False)  # Record delivery + set unpaid
- mark_as_paid()  # Update payment_status to 'paid'
```

### 3. RoundWoodPurchaseOrderItem (Simplified)
```python
Fields:
- purchase_order (FK)
- wood_type (FK)
- quantity_logs
- diameter_inches
- length_feet
- volume_cubic_feet (auto-calculated)
- unit_cost_per_cubic_foot
- subtotal (auto-calculated)
- timestamps

Methods:
- calculate_volume() - volume using log formula
- calculate_subtotal() - subtotal = volume × unit_cost
```

### 4. RoundWoodInventory (Keep as-is)
Used automatically when order is marked delivered
- Tracks current stock
- Cost valuation
- Warehouse location

---

## Simplified Workflow

```
┌──────────┐
│  DRAFT   │  (Create order)
│          │
└────┬─────┘
     │ User clicks "Order"
     ↓
┌──────────┐
│ ORDERED  │  (Sent to supplier, awaiting delivery)
│          │
└────┬─────┘
     │ Goods arrive on [delivery_date]
     │ User clicks "Mark Delivered"
     ↓
┌──────────┐
│DELIVERED │  (In stock, payment pending)
│          │
└────┬─────┘
     │ Pay supplier on delivery date
     │ User clicks "Mark as Paid"
     ↓
  (PAID)    (Order complete)

Optional: Cancel at any point
```

---

## Removed Features
- ❌ No inspection process or inspection_status fields
- ❌ No expected_delivery_date (use delivery_date only)
- ❌ No inspection_date, inspection_notes, inspector_name
- ❌ No ownership_transfer_status
- ❌ No quality_grade on items
- ❌ No quantity_accepted/rejected tracking
- ❌ No approval workflow (created_by only, no approved_by)
- ❌ No RoundWoodProcurementLog (audit trail)
- ❌ No RoundWoodStockTransaction model (keep simple)

---

## API Endpoints (Simplified)

```
POST   /api/round-wood-purchases/              Create order
GET    /api/round-wood-purchases/              List orders
GET    /api/round-wood-purchases/{id}/         Get one order
PATCH  /api/round-wood-purchases/{id}/         Update order
DELETE /api/round-wood-purchases/{id}/         Delete order

POST   /api/round-wood-purchases/{id}/order/   Change status to "ordered"
POST   /api/round-wood-purchases/{id}/deliver/ Mark as delivered + add stock
POST   /api/round-wood-purchases/{id}/pay/     Mark as paid

POST   /api/round-wood-items/                  Add item to order
PATCH  /api/round-wood-items/{id}/             Update item
DELETE /api/round-wood-items/{id}/             Delete item

GET    /api/round-wood-inventory/              View current stock
```

---

## Admin Interface
- List view: po_number, supplier, status, delivery_date, total_amount, payment_status
- Detail view: All fields, inline items
- Filter by: status, supplier, delivery_date, payment_status
- Search by: po_number, po_number_supplier

---

## Key Implementation Points

### Auto-calculate totals
When item added/updated:
```python
item.subtotal = item.volume_cubic_feet * item.unit_cost_per_cubic_foot
item.save()
po.total_amount = sum(item.subtotal for item in po.items.all())
po.save()
```

### Mark Delivered
When status changes to 'delivered':
1. Set actual delivery_date
2. Auto-create RoundWoodInventory entry (or update existing)
3. Set payment_status = 'unpaid' (ready to pay)
4. Do NOT auto-pay (user marks as paid separately)

### Mark as Paid
When payment_status changes to 'paid':
1. Record payment was made
2. No other changes needed

### Stock Management
Simple: On delivery, add all volume to RoundWoodInventory
- No inspection needed
- No acceptance/rejection
- Direct inventory increase

---

## Database Migration Changes
```python
# Remove fields:
- expected_delivery_date
- inspection_date
- inspection_status
- inspection_notes
- inspector_name
- quantity_accepted
- quantity_rejected
- quality_grade
- ownership_transfer_status
- approved_by

# Add fields:
- payment_status (CharField choices: unpaid, paid)

# Keep:
- Everything else
```

---

## Example Workflow

```
1. Create PO (Draft)
   PO#: RWPO-2025-0001
   Supplier: ABC Lumber
   Items: 100 Oak logs @ $50/CF
   Total: $25,000
   Status: Draft

2. Mark as Ordered
   Status changes to: Ordered
   Awaiting delivery...

3. Goods Arrive (Dec 20, 2025)
   User inputs: delivery_date = 2025-12-20
   User clicks: "Mark Delivered"
   - Status → Delivered
   - payment_status → unpaid
   - Auto-add 500 CF to RoundWoodInventory
   - Inventory count updated immediately

4. Pay Supplier (same day)
   User clicks: "Mark as Paid"
   - payment_status → paid
   - Record complete

5. View Order
   RWPO-2025-0001
   Status: Delivered (Paid)
   Order Date: 2025-12-15
   Delivery Date: 2025-12-20
   Amount: $25,000
```

---

## Notes for Implementation

1. **Keep RoundWoodInventory**: Auto-update on delivery. Remove need for manual stock-in.
2. **Simplify views**: No inspection forms, no quality checks, just record + deliver + pay.
3. **Payment tracking**: Add payment_status field so you can query unpaid orders easily.
4. **No audit logs**: Keep timestamps (created_at, updated_at) but remove RoundWoodProcurementLog.
5. **No delivery tracking**: Only one date field (delivery_date) for when goods arrived.

---

## Benefits of Simplified System

✅ Fast to use - 3 status buttons instead of 8  
✅ No inspection delays - goods go straight to inventory  
✅ Clear payment tracking - payment_status shows who needs paying  
✅ Simple to understand - Draft → Ordered → Delivered → Paid  
✅ Less data entry - no inspector name, no quality grades  
✅ Faster transactions - same-day order to payment possible

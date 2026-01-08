# Round Wood Purchasing - Quick Reference

## The 4 Steps

```
1️⃣  DRAFT          Create order + add items
2️⃣  ORDERED        Send to supplier, waiting for delivery
3️⃣  DELIVERED      Goods arrived, auto-added to inventory, unpaid
4️⃣  PAID           Supplier paid, order complete ✅
```

---

## API Quick Guide

### Create & Process Order
```bash
# 1. Create
POST /api/round-wood-purchases/
{ "supplier": 1, "unit_cost_per_cubic_foot": 50.00 }

# 2. Add Item
POST /api/round-wood-items/
{ "purchase_order": 1, "wood_type": 1, "quantity_logs": 100, 
  "diameter_inches": 12, "length_feet": 16 }

# 3. Order
POST /api/round-wood-purchases/1/order/

# 4. Deliver
POST /api/round-wood-purchases/1/deliver/
{ "delivery_date": "2025-12-20" }

# 5. Pay
POST /api/round-wood-purchases/1/pay/
```

### View Data
```bash
# List orders
GET /api/round-wood-purchases/

# Get order details
GET /api/round-wood-purchases/1/

# Check inventory
GET /api/round-wood-inventory/

# Statistics
GET /api/round-wood-purchases/summary/

# Unpaid orders
GET /api/round-wood-purchases/pending_payment/

# Awaiting delivery
GET /api/round-wood-purchases/pending_delivery/
```

---

## Web UI Routes

```
/round-wood/                    Dashboard (summary)
/round-wood/purchase-orders/    List orders
/round-wood/purchase-orders/create/  New order
/round-wood/purchase-orders/1/  Order details
/round-wood/inventory/          Stock levels
/round-wood/wood-types/         Wood types
```

---

## Admin Panel

```
http://localhost:8000/admin/app_round_wood/

- WoodType - View/edit wood species
- RoundWoodPurchaseOrder - Manage orders
- RoundWoodPurchaseOrderItem - Manage items
- RoundWoodInventory - View stock
```

---

## Common Tasks

### Create a Purchase Order
1. Go to `/round-wood/purchase-orders/create/`
2. Select supplier
3. Set unit cost per cubic foot
4. Add notes (optional)
5. Click Create

### Add Items to Order
1. Go to order detail page
2. Click "Add Item"
3. Select wood type
4. Enter quantity, diameter, length
5. Click Save (volume auto-calculates)

### Mark as Ordered
```
Status: Draft → Ordered
Action: Click "Order Now" button
Effect: Ready to be delivered
```

### Mark as Delivered
```
Status: Ordered → Delivered
Action: Click "Mark Delivered", enter date
Effect: Auto-adds all logs to inventory
        payment_status = unpaid
```

### Mark as Paid
```
Status: Delivered → Paid
Action: Click "Mark as Paid"
Effect: Order complete, supplier payment recorded
```

---

## Filter & Search

### By Status
- draft
- ordered
- delivered
- cancelled

### By Payment
- unpaid
- paid

### Search
- PO number (RWPO-2025-0001)
- Supplier name
- Supplier PO number

---

## Inventory Auto-Update

When you mark an order as **Delivered**:
- ✅ All items go to inventory automatically
- ✅ Cost recorded at supplier cost
- ✅ Warehouse location preserved
- ✅ No inspection needed
- ✅ Immediate availability

---

## Key Fields

### Purchase Order
- `po_number` - Auto-generated (RWPO-2025-####)
- `status` - draft, ordered, delivered, cancelled
- `payment_status` - unpaid, paid
- `order_date` - When order created
- `delivery_date` - When goods arrived
- `total_amount` - Sum of all items
- `unit_cost_per_cubic_foot` - ₱/CF

### Order Item
- `quantity_logs` - Number of logs
- `diameter_inches` - Log diameter
- `length_feet` - Log length
- `volume_cubic_feet` - Auto-calculated
- `subtotal` - quantity × unit_cost

---

## Removed Features

❌ Inspections  
❌ Expected delivery dates  
❌ Ownership transfer tracking  
❌ Quality grades  
❌ Acceptance/rejection tracking  
❌ Approval workflow  
❌ Audit logs  
❌ Stock transaction logs  

---

## Useful Links

- Dashboard: `/round-wood/`
- API Root: `/api/round-wood-purchases/`
- Admin: `/admin/app_round_wood/`
- API Docs: `/api/` (if configured)

---

## Volume Formula

```
Volume = π × (diameter/2)² × length × quantity / 12

Example:
- 100 logs, 12" diameter, 16' length
- Volume = 3.14159 × 6² × 16 × 100 / 12
- Volume ≈ 500 cubic feet
```

---

## Status Codes

✅ Draft - Ready to edit  
✅ Ordered - Waiting for delivery  
✅ Delivered - In inventory, payment pending  
✅ Cancelled - Order voided  

---

## Authentication

All API endpoints require:
```
Authorization: Bearer YOUR_TOKEN
```

Get token: Contact admin or use login endpoint

---

## Examples

### API Response: Create Order
```json
{
  "id": 1,
  "po_number": "RWPO-2025-0001",
  "supplier": 1,
  "supplier_name": "ABC Lumber Co",
  "status": "draft",
  "payment_status": "unpaid",
  "order_date": "2025-12-15",
  "delivery_date": null,
  "total_volume_cubic_feet": "0.00",
  "total_amount": "0.00",
  "items": []
}
```

### API Response: Add Item
```json
{
  "id": 5,
  "purchase_order": 1,
  "wood_type": 1,
  "wood_type_name": "Oak",
  "quantity_logs": 100,
  "diameter_inches": "12.00",
  "length_feet": "16.00",
  "volume_cubic_feet": "502.65",
  "unit_cost_per_cubic_foot": "50.00",
  "subtotal": "25132.50"
}
```

---

## Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| "Only draft orders..." | Wrong status | Check current status |
| "Order must have items" | No items | Add items first |
| "Already marked as paid" | Paid twice | Check payment status |
| "Only ordered items..." | Wrong status | Mark as ordered first |

---

## Performance Tips

✅ Use filters to reduce list size  
✅ Batch operations when possible  
✅ Check inventory summary for total values  
✅ Use pending_payment to find unpaid orders  

---

## Database Info

- Model: `RoundWoodPurchaseOrder`
- Items: `RoundWoodPurchaseOrderItem`
- Inventory: `RoundWoodInventory`
- Wood Types: `WoodType`

No transaction or audit log tables.

---

## Support

**Django System Check**
```bash
python manage.py check
# Should show: "System check identified no issues (0 silenced)."
```

**Show Migrations**
```bash
python manage.py showmigrations app_round_wood
# Should show 0003 as applied
```

**Test API**
```bash
curl http://localhost:8000/api/round-wood-purchases/ \
  -H "Authorization: Bearer TOKEN"
```

---

*Last Updated: December 2025*  
*Version: 2.0 (Simplified)*  
*Status: Production Ready ✅*

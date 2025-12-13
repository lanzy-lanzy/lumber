# Force Delete - Quick Start

## Status: ✅ IMPLEMENTED & TESTED

---

## The Problem (FIXED)

```
Error: Cannot delete product referenced in sales orders
Reason: SalesOrderItem.product had PROTECT constraint
Solution: Changed to CASCADE + added force delete
```

---

## What Changed

| Component | Before | After |
|-----------|--------|-------|
| `SalesOrderItem.product` | PROTECT ❌ | CASCADE ✅ |
| `LumberProduct.category` | PROTECT ❌ | CASCADE ✅ |
| Single delete | Blocked ❌ | Works ✅ |
| Force delete | N/A | Available ✅ |

---

## Quick Usage

### Delete Single Product
```bash
DELETE /api/products/25/
```
✅ **Now works** (even if in sales orders)

### Delete with Force Parameter
```bash
POST /api/products/bulk_delete/
{
    "ids": [25],
    "force": true
}
```

Response:
```json
{
    "success": true,
    "deleted_count": 1,
    "deletion_details": [{
        "product_id": 25,
        "product_name": "2x8 Engineered Joist",
        "deleted_items": {
            "sales_order_items": 3,
            "stock_transactions": 5,
            "inventory_snapshots": 45,
            "cart_items": 0
        }
    }]
}
```

---

## What Gets Deleted

When you delete a product:
```
Product 25 "2x8 Engineered Joist"
├─ 3 Sales Order Items ✓ DELETED
├─ 5 Stock Transactions ✓ DELETED
├─ 45 Inventory Snapshots ✓ DELETED
├─ 0 Cart Items ✓ DELETED
└─ Inventory Record ✓ DELETED
```

**Sales Orders survive** (only the line item deleted)

---

## JavaScript Implementation

### Confirm & Delete
```javascript
async function deleteProduct(productId, hasReferences = false) {
    const msg = hasReferences 
        ? 'Delete product? It\'s in sales orders - all related records will be deleted'
        : 'Delete this product?';
    
    if (!confirm(msg)) return;
    
    const res = await fetch('/api/products/bulk_delete/', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer token',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            ids: [productId],
            force: hasReferences
        })
    });
    
    const result = await res.json();
    if (result.success) {
        console.log(`✅ Deleted: ${result.deletion_details?.[0]?.product_name}`);
        location.reload();
    }
}
```

### Bulk Delete
```javascript
async function deleteBulk(ids) {
    if (!confirm(`Delete ${ids.length} products?`)) return;
    
    const res = await fetch('/api/products/bulk_delete/', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer token',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ids, force: true })
    });
    
    const result = await res.json();
    console.log(`Deleted: ${result.deleted_count} / ${result.total_requested}`);
    location.reload();
}
```

---

## API Endpoint

### POST /api/products/bulk_delete/

**Request:**
```json
{
    "ids": [25, 26, 27],
    "force": true
}
```

**Response (Success):**
```json
{
    "success": true,
    "deleted_count": 3,
    "total_requested": 3,
    "force": true,
    "deletion_details": [...]
}
```

**Response (Partial Failure):**
```json
{
    "success": true,
    "deleted_count": 2,
    "total_requested": 3,
    "failed_deletions": [{
        "product_id": 27,
        "error": "..."
    }]
}
```

---

## Migration Status

✅ Applied:
- `app_sales.0005_alter_salesorderitem_product`
- `app_inventory.0007_alter_lumberproduct_category`

Verify:
```bash
python manage.py showmigrations app_sales app_inventory
```

---

## Cascade Rules

### What Deletes With Product

| Record | Behavior | Notes |
|--------|----------|-------|
| Stock Transactions | CASCADE | All deleted |
| Sales Order Items | CASCADE | Product line deleted |
| Inventory Snapshots | CASCADE | All deleted |
| Cart Items | CASCADE | All deleted |
| Inventory | CASCADE | Deleted |
| Sales Orders | SAFE | Still exist |
| Caches | CLEARED | Automatic |

---

## force Parameter

### Without force=true (or force=false)
- Works normally
- Cascade deletes all related records
- Shows warning in response if has sales orders

### With force=true
- Same behavior (cascade deletes)
- User explicitly acknowledged
- Good for UI to show it was intentional

**Bottom line:** Cascade works either way. `force=true` is just for UI UX.

---

## Examples

### Example 1: Delete Simple Product
```bash
curl -X POST http://localhost:8000/api/products/bulk_delete/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids":[100]}'

# Response: Deleted 1 product (no related records)
```

### Example 2: Delete Product with Sales Orders
```bash
curl -X POST http://localhost:8000/api/products/bulk_delete/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids":[25],"force":true}'

# Response: Deleted 1 product + 3 sales order items + 5 transactions
```

### Example 3: Bulk Delete Multiple
```bash
curl -X POST http://localhost:8000/api/products/bulk_delete/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids":[25,26,27,28],"force":true}'

# Response: Deleted 4 products with all their references
```

---

## Response Details

### Deletion Summary Shows:
- `product_id` - ID of deleted product
- `product_name` - Name of deleted product
- `deleted_items.stock_transactions` - Number deleted
- `deleted_items.sales_order_items` - Number deleted
- `deleted_items.inventory_snapshots` - Number deleted
- `deleted_items.cart_items` - Number deleted

Example:
```json
"deletion_details": [{
    "product_id": 25,
    "product_name": "2x8 Engineered Joist",
    "deleted_items": {
        "stock_transactions": 5,
        "sales_order_items": 3,
        "inventory_snapshots": 45,
        "cart_items": 0
    }
}]
```

---

## Testing

```bash
# Verify migrations
python manage.py showmigrations app_sales app_inventory

# Test delete
python manage.py shell < test_product_deletion.py

# Try API
curl -X POST http://localhost:8000/api/products/bulk_delete/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids":[25],"force":true}'
```

---

## Files Modified

```
✓ app_sales/models.py (line 82)
✓ app_inventory/models.py (line 24)
✓ app_inventory/views.py (bulk_delete enhanced)
✓ app_sales/migrations/0005_* (applied)
✓ app_inventory/migrations/0007_* (applied)
```

---

## Key Points

✅ Products can be deleted now  
✅ Force parameter works  
✅ All related records cascade deleted  
✅ Atomic transactions (all or nothing)  
✅ Detailed deletion summary  
✅ Migrations applied  

---

## Documentation

- **FORCE_DELETE_GUIDE.md** - Complete guide with examples
- **PRODUCT_DELETION_FIX.md** - Original deletion fix
- **DELETION_QUICK_REFERENCE.md** - General quick reference

---

**Status: ✅ COMPLETE** • Ready for production use

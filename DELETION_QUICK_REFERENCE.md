# Quick Reference: Product Deletion

## The Problem (FIXED)
```
ProtectedError: Cannot delete some instances of model 'LumberProduct' 
because they are referenced through protected foreign keys: 'StockTransaction.product'
```

## The Solution ✅

### Single Product Delete
```bash
curl -X DELETE http://localhost:8000/api/products/2/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```
**Status:** ✓ Now works (cascade deletes related transactions)

### Bulk Delete Multiple Products
```bash
curl -X POST http://localhost:8000/api/products/bulk_delete/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids": [1, 2, 3]}'
```

**Response:**
```json
{
    "success": true,
    "deleted_count": 3,
    "total_requested": 3
}
```

## What Changed

| Component | Before | After |
|-----------|--------|-------|
| `StockTransaction.product` | `on_delete=PROTECT` | `on_delete=CASCADE` |
| Product deletion | ❌ Blocked | ✅ Works |
| Bulk delete | ❌ N/A | ✅ Available |
| Migration | — | ✓ Applied |

## Cascade Behavior

When you delete a product:
- Product → **Deleted**
- Inventory → **Deleted** (CASCADE)
- Stock Transactions → **Deleted** (CASCADE)
- Inventory Snapshots → **Deleted** (CASCADE)
- Caches → **Cleared**

## JavaScript Example (Frontend)

```javascript
// Single delete
const productId = 2;
const response = await fetch(`/api/products/${productId}/`, {
    method: 'DELETE',
    headers: {
        'Authorization': 'Bearer token',
        'X-CSRFToken': csrfToken
    }
});

// Bulk delete
const response = await fetch('/api/products/bulk_delete/', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer token',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({ ids: [1, 2, 3] })
});
```

## Django Shell Test

```bash
python manage.py shell

from app_inventory.models import LumberProduct
product = LumberProduct.objects.first()
print(f"Deleting {product.name}...")
product.delete()  # Will cascade delete all related transactions!
```

## Files Modified

1. **app_inventory/models.py** - Line 83
2. **app_inventory/views.py** - Added bulk_delete action (lines 135-202)
3. **app_inventory/migrations/0006_alter_stocktransaction_product.py** - New migration

## Testing

```bash
# Run migration
python manage.py migrate app_inventory

# Test endpoint
curl -X POST http://localhost:8000/api/products/bulk_delete/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids": [1]}'
```

## Status
- ✅ Migration applied
- ✅ Model updated
- ✅ Endpoint available
- ✅ Cascade tested
- ⏳ Frontend UI (optional - see BULK_DELETE_UI_GUIDE.md)

## Help & Documentation

| Document | Purpose |
|----------|---------|
| PRODUCT_DELETION_FIX.md | Detailed technical docs |
| BULK_DELETE_UI_GUIDE.md | Frontend implementation |
| test_product_deletion.py | Automated tests |
| DELETION_QUICK_REFERENCE.md | This file |

---

**TL;DR:** Products can now be deleted. Use POST `/api/products/bulk_delete/` with `{"ids": [1,2,3]}` to delete multiple.

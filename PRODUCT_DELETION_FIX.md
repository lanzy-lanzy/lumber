# Product Deletion Fix & Bulk Delete Implementation

## Problem
When attempting to delete a product, the system threw a `ProtectedError` because `StockTransaction` objects had a PROTECT constraint on the product foreign key.

**Error:**
```
django.db.models.deletion.ProtectedError: ("Cannot delete some instances of model 'LumberProduct' because they are referenced through protected foreign keys: 'StockTransaction.product'."
```

## Solution Implemented

### 1. Changed Foreign Key Cascade Behavior
**File:** `app_inventory/models.py`

Changed `StockTransaction.product` from `PROTECT` to `CASCADE`:
```python
# Before
product = models.ForeignKey(LumberProduct, on_delete=models.PROTECT, related_name='stock_transactions')

# After
product = models.ForeignKey(LumberProduct, on_delete=models.CASCADE, related_name='stock_transactions')
```

**Why CASCADE?**
- When a product is deleted, all its related stock transactions are automatically deleted
- This maintains data integrity while allowing product deletion
- Cascading deletes are atomic (all-or-nothing)

### 2. Applied Database Migration
Created and applied migration: `app_inventory/migrations/0006_alter_stocktransaction_product.py`

Run this command to apply the migration:
```bash
python manage.py migrate app_inventory
```

### 3. Implemented Bulk Delete Endpoint
**File:** `app_inventory/views.py` → `LumberProductViewSet.bulk_delete()`

**Endpoint:** `POST /api/products/bulk_delete/`

**Payload:**
```json
{
    "ids": [1, 2, 3],
    "force": false
}
```

**Features:**
- Delete multiple products in a single atomic transaction
- Automatic cascade deletion of related stock transactions
- Comprehensive error handling with partial success support
- Automatic cache clearing after deletion
- Returns detailed response with deletion count and any failures

**Response (Success):**
```json
{
    "success": true,
    "deleted_count": 3,
    "total_requested": 3
}
```

**Response (Partial Success):**
```json
{
    "success": true,
    "deleted_count": 2,
    "total_requested": 3,
    "failed_deletions": [
        {
            "product_id": 5,
            "product_name": "Product Name",
            "error": "Error message"
        }
    ]
}
```

## Usage Examples

### Single Product Deletion (Frontend)
```javascript
// This now works without ProtectedError
await fetch(`/api/products/2/`, {
    method: 'DELETE',
    headers: {'Authorization': 'Bearer token'}
});
```

### Bulk Delete Multiple Products
```javascript
const productIds = [1, 2, 3];
const response = await fetch('/api/products/bulk_delete/', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        ids: productIds
    })
});

const result = await response.json();
console.log(`Deleted ${result.deleted_count} products`);
```

## What Gets Deleted

When a product is deleted:
1. **Product record** - The LumberProduct itself
2. **Inventory record** - Related Inventory (uses CASCADE)
3. **Stock Transactions** - All StockTransaction records (now uses CASCADE)
4. **Inventory Snapshots** - Historical snapshots (uses CASCADE)
5. **Caches** - All product-related caches are cleared

## Safety Considerations

✅ **Atomic Transactions:** Bulk deletes are wrapped in database transactions - either all succeed or none do

✅ **Data Cascade:** Automatically cleans up dependent records to maintain referential integrity

✅ **Error Handling:** Individual failures don't prevent deletion of other products

✅ **Cache Management:** Automatically invalidates related caches after deletion

⚠️ **No Undo:** Deleted data is permanently removed. Consider archiving instead if you need to preserve history

## Related Configuration

### Cascade Dependencies in System:
```
LumberProduct
├── Inventory (CASCADE)
├── StockTransaction (CASCADE)
├── InventorySnapshot (CASCADE)
└── LumberCategory (PROTECT - must delete category first if needed)
```

## Testing the Fix

### Test Single Deletion:
```bash
curl -X DELETE http://localhost:8000/api/products/2/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test Bulk Deletion:
```bash
curl -X POST http://localhost:8000/api/products/bulk_delete/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids": [1, 2, 3]}'
```

## Migration Rollback (if needed)

To revert the CASCADE change:
```bash
python manage.py migrate app_inventory 0005
```

This will restore the PROTECT constraint, preventing product deletion until related transactions are handled.

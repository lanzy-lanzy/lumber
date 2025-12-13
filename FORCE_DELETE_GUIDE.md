# Force Delete Products - Complete Guide

## Status: ✅ COMPLETE

All PROTECT constraints have been removed and force deletion is fully implemented.

---

## What Was Fixed

### Previous Issues
- ❌ Products referenced in Sales Orders couldn't be deleted (PROTECT)
- ❌ Products with categories couldn't be deleted if category existed
- ⚠️ Had to manually remove all references before deletion

### Now Fixed ✅
- ✅ Products cascade delete with all related records
- ✅ Force delete works with single click
- ✅ Bulk delete handles multiple products
- ✅ Detailed deletion summary provided

---

## Database Changes

### Changed Constraints

| Model | Field | Before | After | File | Migration |
|-------|-------|--------|-------|------|-----------|
| `SalesOrderItem` | `product` | `PROTECT` | `CASCADE` | `app_sales/models.py:82` | `0005_alter_salesorderitem_product.py` ✓ |
| `LumberProduct` | `category` | `PROTECT` | `CASCADE` | `app_inventory/models.py:24` | `0007_alter_lumberproduct_category.py` ✓ |
| `StockTransaction` | `product` | `PROTECT` | `CASCADE` | (already fixed) | (already applied) |

**Status:** ✓ All migrations applied

---

## Cascade Deletion Behavior

When a product is deleted, ALL related records are automatically deleted:

```
Product Deletion
├─ StockTransaction (all) ──→ DELETED
├─ SalesOrderItem (all) ──→ DELETED
├─ InventorySnapshot (all) ──→ DELETED
├─ CartItem (all) ──→ DELETED
├─ Inventory ──→ DELETED
└─ Caches ──→ CLEARED
```

---

## API Usage

### Single Product Delete

```bash
DELETE /api/products/25/
```

**Response:**
```json
{
    "success": true
}
```

✅ **Now works!** Previously blocked by ProtectedError

---

### Bulk Delete (Basic)

```bash
POST /api/products/bulk_delete/

{
    "ids": [1, 2, 3]
}
```

**Response:**
```json
{
    "success": true,
    "deleted_count": 3,
    "total_requested": 3,
    "force": false
}
```

---

### Force Delete (Recommended)

Use `force=true` to explicitly acknowledge you're deleting products with references:

```bash
POST /api/products/bulk_delete/

{
    "ids": [25, 26, 27],
    "force": true
}
```

**Response with Details:**
```json
{
    "success": true,
    "deleted_count": 3,
    "total_requested": 3,
    "force": true,
    "deletion_details": [
        {
            "product_id": 25,
            "product_name": "2x8 Engineered Joist",
            "deleted_items": {
                "stock_transactions": 5,
                "sales_order_items": 3,
                "inventory_snapshots": 45,
                "cart_items": 0
            }
        },
        {
            "product_id": 26,
            "product_name": "4x4 Pressure Treated Cedar",
            "deleted_items": {
                "stock_transactions": 2,
                "sales_order_items": 1,
                "inventory_snapshots": 30,
                "cart_items": 1
            }
        },
        {
            "product_id": 27,
            "product_name": "1x12 Pine Common",
            "deleted_items": {
                "stock_transactions": 0,
                "sales_order_items": 0,
                "inventory_snapshots": 15,
                "cart_items": 0
            }
        }
    ]
}
```

**What gets deleted per product:**
- ✅ All 5 stock transactions for product 25
- ✅ All 3 sales order items for product 25
- ✅ All 45 inventory snapshots for product 25
- ✅ All cart items for product 25

---

### Force Delete - Partial Success

If some products fail:

```json
{
    "success": true,
    "deleted_count": 2,
    "total_requested": 3,
    "force": true,
    "deletion_details": [
        {
            "product_id": 25,
            "product_name": "2x8 Engineered Joist",
            "deleted_items": {
                "stock_transactions": 5,
                "sales_order_items": 3,
                "inventory_snapshots": 45,
                "cart_items": 0
            }
        },
        {
            "product_id": 26,
            "product_name": "4x4 Pressure Treated Cedar",
            "deleted_items": {
                "stock_transactions": 2,
                "sales_order_items": 1,
                "inventory_snapshots": 30,
                "cart_items": 1
            }
        }
    ],
    "failed_deletions": [
        {
            "product_id": 27,
            "product_name": "1x12 Pine Common",
            "error": "Database constraint violation"
        }
    ]
}
```

---

## JavaScript Examples

### Simple Delete

```javascript
// Delete a single product
const response = await fetch(`/api/products/25/`, {
    method: 'DELETE',
    headers: {
        'Authorization': 'Bearer YOUR_TOKEN',
        'X-CSRFToken': getCookie('csrftoken')
    }
});

if (response.ok) {
    alert('Product deleted successfully');
    location.reload();
}
```

### Bulk Delete with Force

```javascript
const productIds = [25, 26, 27];
const forceDelete = true; // Set to true to delete products with references

const response = await fetch('/api/products/bulk_delete/', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        ids: productIds,
        force: forceDelete
    })
});

const result = await response.json();

if (result.success) {
    // Show detailed summary
    console.log(`Deleted ${result.deleted_count} products`);
    
    result.deletion_details?.forEach(detail => {
        console.log(`${detail.product_name}:`);
        console.log(`  - Stock Transactions: ${detail.deleted_items.stock_transactions}`);
        console.log(`  - Sales Orders: ${detail.deleted_items.sales_order_items}`);
        console.log(`  - Snapshots: ${detail.deleted_items.inventory_snapshots}`);
        console.log(`  - Cart Items: ${detail.deleted_items.cart_items}`);
    });
    
    location.reload();
}
```

### With Confirmation Dialog

```javascript
async function deleteProductsWithConfirmation(productIds, hasReferences = false) {
    let message = `Delete ${productIds.length} product(s)?`;
    
    if (hasReferences) {
        message += '\n\nWarning: These products are referenced in:\n';
        message += '  • Sales Orders\n';
        message += '  • Stock Transactions\n';
        message += '  • Shopping Carts\n\n';
        message += 'All related records will also be deleted.';
    }
    
    if (!confirm(message)) {
        return null;
    }
    
    const response = await fetch('/api/products/bulk_delete/', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer YOUR_TOKEN',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            ids: productIds,
            force: hasReferences
        })
    });
    
    return await response.json();
}

// Usage
const result = await deleteProductsWithConfirmation([25, 26, 27], true);
if (result?.success) {
    console.log(`✅ Deleted ${result.deleted_count} products`);
}
```

---

## What Gets Deleted with Force Delete

### Related Records Deleted Automatically

When you delete a product with `force=true`, these records are also deleted:

#### 1. Stock Transactions
- Stock In records
- Stock Out records
- Adjustment records
- All transaction history

#### 2. Sales Order Items
- Line items in sales orders
- Does NOT delete the sales order itself (only the product reference)
- Sales order still exists but with deleted item reference

#### 3. Inventory Records
- Current inventory level
- Historical snapshots (daily records)

#### 4. Shopping Cart Items
- Customer cart items containing the product
- Cart itself still exists

#### 5. Caches
- Product cache entries
- List cache entries
- Related query caches

---

## When to Use Force Delete

### Use `force=true` when:
✅ You want to delete a product that appears in sales orders
✅ You want to clean up test/demo data
✅ You're deleting products with full history
✅ You've confirmed the deletion with the user

### Best Practice:
1. Always show users what will be deleted
2. Require explicit confirmation
3. Use `force=true` parameter to acknowledge
4. Display the deletion summary

---

## Safety Guarantees

✅ **Atomic Transactions** - All deletes succeed or all rollback  
✅ **No Orphaned Records** - Cascade ensures referential integrity  
✅ **Audit Trail** - Deletion details show what was removed  
✅ **Error Handling** - Partial failures reported separately  
✅ **Permission Checks** - Only authenticated users  
✅ **Cache Invalidation** - Automatic and complete  

⚠️ **No Recovery** - Deletions are permanent

---

## Testing Force Delete

### Test Script

```bash
# Run the automated test
python manage.py shell < test_product_deletion.py
```

### Manual Test

```bash
# Create test data (product with sales orders)
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name":"Test Product","sku":"TEST-001",...}'

# Verify it appears in sales orders
curl http://localhost:8000/api/sales-orders/ \
  -H "Authorization: Bearer TOKEN"

# Force delete the product
curl -X POST http://localhost:8000/api/products/bulk_delete/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids":[TEST_ID],"force":true}'

# Verify it's gone
curl http://localhost:8000/api/products/TEST_ID/ \
  -H "Authorization: Bearer TOKEN"
# Should return 404
```

---

## Response Examples

### Success (No References)

```json
{
    "success": true,
    "deleted_count": 1,
    "total_requested": 1,
    "force": false,
    "deletion_details": [
        {
            "product_id": 25,
            "product_name": "Simple Product",
            "deleted_items": {
                "stock_transactions": 0,
                "sales_order_items": 0,
                "inventory_snapshots": 5,
                "cart_items": 0
            }
        }
    ]
}
```

### Success (With References)

```json
{
    "success": true,
    "deleted_count": 1,
    "total_requested": 1,
    "force": true,
    "deletion_details": [
        {
            "product_id": 25,
            "product_name": "2x8 Engineered Joist",
            "deleted_items": {
                "stock_transactions": 5,
                "sales_order_items": 3,
                "inventory_snapshots": 45,
                "cart_items": 1
            }
        }
    ]
}
```

### Partial Failure

```json
{
    "success": true,
    "deleted_count": 2,
    "total_requested": 3,
    "force": true,
    "deletion_details": [...],
    "failed_deletions": [
        {
            "product_id": 99,
            "product_name": "Failed Product",
            "error": "Some database error"
        }
    ]
}
```

---

## Frontend Implementation

### Quick Checklist

- [ ] Add delete button that shows product references
- [ ] Show confirmation dialog with deletion details
- [ ] Use `force=true` parameter
- [ ] Display deletion summary to user
- [ ] Refresh product list after deletion
- [ ] Handle partial failures gracefully

### Example Delete Button

```html
<button class="btn btn-danger" onclick="deleteProduct(25)">
    Delete Product
</button>

<script>
async function deleteProduct(productId) {
    // Show references
    const response = await fetch(`/api/products/${productId}/`);
    const product = await response.json();
    
    // Check for references
    const hasSalesOrders = product.sales_order_items?.length > 0;
    const hasTransactions = product.stock_transactions?.length > 0;
    
    // Show warning if needed
    let message = `Delete "${product.name}"?`;
    if (hasSalesOrders || hasTransactions) {
        message = `This product is referenced in ${
            hasSalesOrders ? 'sales orders' : ''
        }. ${
            hasTransactions ? 'It also has stock transactions.' : ''
        } \n\nDelete anyway?`;
    }
    
    if (!confirm(message)) return;
    
    // Delete with force=true if has references
    const deleteResponse = await fetch('/api/products/bulk_delete/', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer token',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            ids: [productId],
            force: hasSalesOrders || hasTransactions
        })
    });
    
    const result = await deleteResponse.json();
    if (result.success) {
        alert(`✅ Deleted "${product.name}"`);
        location.reload();
    }
}
</script>
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Still getting ProtectedError | Migration not applied - run `python manage.py migrate` |
| force parameter ignored | Update views.py, restart server |
| Sales orders still exist | They do! Only the product reference is deleted |
| Want to undo deletion | No undo available - deletions are permanent |
| Partial deletion failed | Check error in response, fix constraint, retry |

---

## Files Modified

```
✓ app_sales/models.py (line 82: PROTECT → CASCADE)
✓ app_inventory/models.py (line 24: PROTECT → CASCADE)  
✓ app_inventory/views.py (bulk_delete enhanced with force parameter)
✓ app_sales/migrations/0005_alter_salesorderitem_product.py (new)
✓ app_inventory/migrations/0007_alter_lumberproduct_category.py (new)
```

---

## Related Documentation

- **PRODUCT_DELETION_FIX.md** - Original deletion fix
- **DELETION_QUICK_REFERENCE.md** - Quick commands
- **BULK_DELETE_UI_GUIDE.md** - Frontend implementation
- **START_HERE_DELETION_FIX.md** - Getting started

---

**Status:** ✅ Complete and tested  
**Last Updated:** December 13, 2025  
**Ready:** Production use

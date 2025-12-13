# Bulk Delete UI Implementation Guide

## Quick Implementation for Products Page

### HTML Changes
Add checkboxes to your products table and bulk delete button:

```html
<div class="table-controls">
    <button id="bulkDeleteBtn" class="btn btn-danger" style="display:none;">
        Delete Selected (<span id="selectedCount">0</span>)
    </button>
</div>

<table class="table">
    <thead>
        <tr>
            <th>
                <input type="checkbox" id="selectAllCheckbox">
            </th>
            <th>Image</th>
            <th>SKU</th>
            <th>Product Name</th>
            <!-- ... other columns ... -->
        </tr>
    </thead>
    <tbody>
        <!-- Repeat for each product row -->
        <tr>
            <td>
                <input type="checkbox" class="product-checkbox" data-product-id="{{product.id}}">
            </td>
            <td><img src="{{product.image.url}}" alt="{{product.name}}"></td>
            <!-- ... rest of row ... -->
        </tr>
    </tbody>
</table>
```

### JavaScript Implementation

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
    const productCheckboxes = document.querySelectorAll('.product-checkbox');
    const bulkDeleteBtn = document.getElementById('bulkDeleteBtn');
    const selectedCountSpan = document.getElementById('selectedCount');

    // Select all functionality
    selectAllCheckbox.addEventListener('change', function() {
        productCheckboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
        updateBulkDeleteButton();
    });

    // Individual checkbox change
    productCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateBulkDeleteButton);
    });

    // Update button visibility and count
    function updateBulkDeleteButton() {
        const selectedCount = Array.from(productCheckboxes).filter(cb => cb.checked).length;
        selectedCountSpan.textContent = selectedCount;
        bulkDeleteBtn.style.display = selectedCount > 0 ? 'block' : 'none';
    }

    // Bulk delete handler
    bulkDeleteBtn.addEventListener('click', async function() {
        const selectedIds = Array.from(productCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => parseInt(cb.dataset.productId));

        if (selectedIds.length === 0) {
            alert('No products selected');
            return;
        }

        // Confirmation dialog
        if (!confirm(`Are you sure you want to delete ${selectedIds.length} product(s)? This will also delete all related stock transactions.`)) {
            return;
        }

        try {
            bulkDeleteBtn.disabled = true;
            bulkDeleteBtn.textContent = 'Deleting...';

            const response = await fetch('/api/products/bulk_delete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    ids: selectedIds
                })
            });

            const result = await response.json();

            if (response.ok) {
                // Success
                const message = `Successfully deleted ${result.deleted_count} product(s)`;
                
                if (result.failed_deletions && result.failed_deletions.length > 0) {
                    alert(`${message}\n\nFailed: ${result.failed_deletions.length} products`);
                } else {
                    alert(message);
                }

                // Reload the page to refresh the list
                location.reload();
            } else {
                alert(`Error: ${result.error || 'Failed to delete products'}`);
            }
        } catch (error) {
            console.error('Delete error:', error);
            alert('An error occurred while deleting products');
        } finally {
            bulkDeleteBtn.disabled = false;
            bulkDeleteBtn.textContent = 'Delete Selected';
        }
    });

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
```

### CSS Styling (Optional)

```css
.table-controls {
    margin-bottom: 20px;
    padding: 10px;
    background-color: #f8f9fa;
    border-radius: 4px;
}

#bulkDeleteBtn {
    margin-left: auto;
}

.table tbody tr:hover {
    background-color: #f5f5f5;
}

.product-checkbox {
    width: 18px;
    height: 18px;
    cursor: pointer;
}
```

## Backend Permissions

Ensure your user has the proper permissions to delete products:

```python
# In your template/view context check
if request.user.has_perm('app_inventory.delete_lumberproduct'):
    # Show delete UI
```

## Integration Points

### With Existing Delete Button
If you already have individual delete buttons:

```javascript
// Existing single product delete
const deleteBtn = document.querySelector('[data-action="delete"]');
if (deleteBtn) {
    deleteBtn.addEventListener('click', async function() {
        const productId = this.dataset.productId;
        
        if (!confirm('Delete this product?')) return;
        
        // Use bulk_delete endpoint with single ID
        await fetch('/api/products/bulk_delete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                ids: [parseInt(productId)]
            })
        });
    });
}
```

## Example: Django Template Integration

```django
{% if user.has_perm 'app_inventory.delete_lumberproduct' %}
<div class="bulk-actions">
    <button id="selectAllBtn" class="btn btn-sm btn-outline">
        <input type="checkbox" id="selectAllCheckbox"> Select All
    </button>
    <button id="bulkDeleteBtn" class="btn btn-danger" style="display:none;">
        Delete Selected (<span id="selectedCount">0</span>)
    </button>
</div>
{% endif %}
```

## Response Handling Examples

### Show Progress
```javascript
// For larger batches, show progress
const totalProducts = selectedIds.length;
const progressBar = document.createElement('div');
progressBar.className = 'progress';
// ... update as deletion progresses
```

### Selective Deletion
```javascript
// Only delete products that match criteria
const productsToDelete = selectedIds.filter(id => {
    const row = document.querySelector(`input[data-product-id="${id}"]`).closest('tr');
    const status = row.querySelector('[data-field="status"]').textContent;
    return status === 'Active'; // Only delete active products
});
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CSRF token error | Ensure `getCookie('csrftoken')` is called correctly |
| 403 Forbidden | Check user permissions for product deletion |
| Checkboxes not working | Verify `.product-checkbox` class selector matches table |
| Bulk delete not found | Ensure your Django app is up to date |

## Related API Endpoints

- `DELETE /api/products/{id}/` - Delete single product
- `POST /api/products/bulk_delete/` - Delete multiple products
- `GET /api/products/` - List products
- `POST /api/products/` - Create product

## See Also
- [Product Deletion Fix](./PRODUCT_DELETION_FIX.md)
- [Inventory Management](./INVENTORY_MANAGEMENT.md)

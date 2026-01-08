# Auto-Generated PO Numbers & Default COD Payment Terms

## Features Implemented

### 1. Auto-Generated PO Numbers

No more manual typing of PO numbers! The system now automatically generates unique PO numbers.

#### Format
```
RWPO-YYYY-NNNN
```

**Example:**
- RWPO-2024-0001 (First PO in 2024)
- RWPO-2024-0002 (Second PO in 2024)
- RWPO-2024-0003 (Third PO in 2024)
- RWPO-2025-0001 (First PO in 2025)

#### How It Works

1. **Automatic Generation**: When you create a purchase order, the system automatically generates a unique PO number
2. **Sequential**: Numbers are sequential within each year
3. **No Manual Entry**: The PO Number field is removed from the form
4. **Visible After Creation**: The generated number is shown in confirmation message and on the order detail page

#### Technical Details

```python
# In models.py - RoundWoodPurchaseOrder.save()
def save(self, *args, **kwargs):
    if not self.po_number:
        year = datetime.now().year
        count = RoundWoodPurchaseOrder.objects.filter(
            created_at__year=year
        ).count()
        self.po_number = f"RWPO-{year}-{count + 1:04d}"
    super().save(*args, **kwargs)
```

### 2. Default Payment Terms: Cash on Delivery (COD)

Payment terms now default to "Cash on Delivery (COD)" instead of being empty.

#### How It Works

1. **Default Value**: All new purchase orders automatically have "Cash on Delivery (COD)" as payment terms
2. **Editable**: You can change it to other terms (Net 30, 50% Advance, etc.) if needed
3. **Field Pre-filled**: The Payment Terms field comes pre-filled with COD

#### Usage

**Creating a Purchase Order:**
- The Payment Terms field will already contain "Cash on Delivery (COD)"
- You can edit it to other payment terms if needed
- Leave it as-is to accept the default COD terms

**Examples of Other Terms:**
- `Net 30` - Payment due in 30 days
- `Net 60` - Payment due in 60 days
- `50% Advance, 50% on Delivery` - Half now, half later
- `2/10 Net 30` - 2% discount if paid in 10 days, otherwise due in 30 days
- `Advance Payment` - Full payment before delivery

## Changes Made

### Model Changes
**File:** `app_round_wood/models.py`

1. **PO Number Field**
   - Changed `blank=False` to `blank=True`
   - Added help text: "Auto-generated PO number"
   - Made unique constraint

2. **Payment Terms Field**
   - Added default: `default='Cash on Delivery (COD)'`
   - Changed from optional to having a default value

3. **Save Method**
   - Added `save()` method to generate PO numbers
   - Uses current year and sequential count
   - Ensures no duplicates

### View Changes
**File:** `app_round_wood/views_ui.py`

1. **purchase_order_create()**
   - Removed PO number extraction from POST data
   - Removed PO number from create() call
   - Updated success message to use `po.po_number`
   - Set default payment_terms fallback to COD

### Template Changes
**File:** `templates/round_wood/purchase_order_create.html`

1. **Removed PO Number Field**
   - Shows blue info box instead
   - Explains auto-generation feature

2. **Updated Payment Terms Field**
   - Pre-filled with "Cash on Delivery (COD)"
   - Added "(Default: COD)" to helper text

## Migration

The changes were applied via Django migration:
```
Applying app_round_wood.0002_alter_roundwoodpurchaseorder_payment_terms_and_more
```

## Benefits

### For Users
✅ **Less Typing**: No need to manually create PO numbers
✅ **Consistency**: All PO numbers follow the same format
✅ **Quick Form**: Form creation is now faster
✅ **Default COD**: Most orders use COD, so no need to type it

### For Business
✅ **Standardization**: All POs have consistent numbering
✅ **No Duplicates**: System prevents duplicate PO numbers
✅ **Audit Trail**: Auto-generation is tracked automatically
✅ **Year-Based**: Easy to identify when orders were created

## Examples

### Creating a Purchase Order

**Before (Manual Entry):**
```
PO Number: RWPO-2024-001 (user types this)
Supplier: Oak Supplier Inc
Delivery Date: 2024-12-25
Unit Cost: ₱50.00/CF
Payment Terms: Cash on Delivery (COD) (user types this)
Notes: Standard delivery
```

**After (Auto-Generated):**
```
[Auto-generated: RWPO-2024-0001]
Supplier: Oak Supplier Inc
Delivery Date: 2024-12-25
Unit Cost: ₱50.00/CF
Payment Terms: Cash on Delivery (COD) (pre-filled)
Notes: Standard delivery
```

### Confirmation Message

```
Purchase order RWPO-2024-0001 created successfully
[View Order] [Create Another]
```

## Accessing Auto-Generated PO Numbers

### In Purchase Order Form
The form shows:
```
PO Number will be auto-generated (e.g., RWPO-2024-0001)
```

### After Creation
- Confirmation message shows the generated number
- Order detail page displays it at the top
- List page shows all PO numbers
- API returns the number in responses

### In Database
All PO numbers are stored in the `po_number` field:
```sql
SELECT po_number, supplier, created_at FROM round_wood_purchaseorder 
ORDER BY created_at DESC;
```

## API Usage

### Create Purchase Order via API
```bash
curl -X POST \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "supplier": 1,
    "expected_delivery_date": "2024-12-25",
    "unit_cost_per_cubic_foot": 50.00,
    "payment_terms": "Cash on Delivery (COD)",
    "notes": "Standard delivery"
  }' \
  http://localhost:8000/api/round-wood-purchases/
```

**Response:**
```json
{
  "id": 1,
  "po_number": "RWPO-2024-0001",
  "supplier": 1,
  "payment_terms": "Cash on Delivery (COD)",
  "status": "draft",
  ...
}
```

### Update Payment Terms
```bash
curl -X PATCH \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_terms": "Net 30"
  }' \
  http://localhost:8000/api/round-wood-purchases/1/
```

## Reverting to Manual Entry

If you want to manually specify PO numbers instead of auto-generating them:

1. **Edit Model:**
   ```python
   # In models.py
   po_number = models.CharField(max_length=50, unique=True)  # Remove blank=True
   
   # Remove or comment out the save() method
   ```

2. **Update View:**
   ```python
   # In views_ui.py
   po_number = request.POST.get('po_number')
   po = RoundWoodPurchaseOrder.objects.create(
       po_number=po_number,  # Add back
       ...
   )
   ```

3. **Update Template:**
   - Add back the PO Number input field

4. **Create New Migration:**
   ```bash
   python manage.py makemigrations app_round_wood
   python manage.py migrate app_round_wood
   ```

## Troubleshooting

### Issue: PO Numbers Not Sequential

**Solution:** The count is based on POs created in the current year. Year changes reset the counter.

### Issue: Duplicate PO Numbers

**Solution:** The database constraint (unique=True) prevents this. If you see an error, contact support.

### Issue: Can't Change Payment Terms

**Solution:** Payment Terms is a regular CharField, you can edit it anytime in the detail view or via API.

## Future Enhancements

1. **Custom Prefix**: Allow per-supplier or per-department PO prefixes
2. **Sequential Range**: Set starting numbers for each year
3. **Payment Term Templates**: Create predefined payment term options
4. **Approval Workflow**: Different terms for different suppliers
5. **Automatic Numbering**: Reset counter at year end

## Summary

The auto-generation of PO numbers and default COD payment terms makes the purchase order creation process faster and more consistent. The system handles all the numbering logic, letting you focus on the important details of your orders.

---

**Version:** 1.0
**Date:** 2024
**Status:** Implemented and Active

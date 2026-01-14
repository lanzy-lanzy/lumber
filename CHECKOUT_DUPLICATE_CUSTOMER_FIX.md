# Checkout Duplicate Customer Fix

## Problem
When attempting to checkout, you get the error:
```
MultipleObjectsReturned: get() returned more than one Customer -- it returned 2!
```

## Root Cause
The `Customer` model's `email` field was not unique, allowing multiple customers with the same email address. When the checkout endpoint tried to get or create a customer using only the email, Django's `.get()` method failed because it returned multiple matches.

## Solution

### 1. Model Changes (app_sales/models.py)
Changed the email field to be unique and nullable:
```python
email = models.EmailField(blank=True, unique=True, null=True)
```

### 2. New Migration (app_sales/migrations/0010_remove_duplicate_customers.py)
This migration:
- Removes duplicate customers, keeping the oldest one
- Adds the unique constraint to the email field

### 3. Updated Checkout Code (app_sales/cart_views.py)
Enhanced error handling in the checkout method to:
- Check if email is empty before using it for lookup
- Fall back to using the customer name if email is empty
- This prevents future issues with customers missing emails

## To Apply This Fix

### Step 1: Run the Migration
```bash
python manage.py migrate
```

This will:
- Find all duplicate customers with the same email
- Reassign any orders/related data from duplicate customers to the original customer
- Remove duplicate customers
- Add the unique constraint to the email field

### Step 2: Verify the Fix
Try checking out again. The checkout should now work correctly.

## Troubleshooting

If the migration fails with a `ProtectedError`, the script will:
1. Reassign all `LumberingServiceOrder` records to the kept customer
2. Reassign all `OrderNotification` records to the kept customer  
3. Reassign all `OrderConfirmation` records to the kept customer
4. Then delete the duplicate customer

## Alternative: Manual Cleanup (if migration has issues)

If the migration fails or you want to manually clean up duplicates first:

### Using the Provided Script:

```bash
python manage.py shell < manual_duplicate_customer_fix.py
```

This script will:
- Display all duplicate customers
- Show how many related orders each duplicate has
- Reassign all orders to the original customer
- Delete the duplicates
- Show a summary of what was fixed

### Or Manually in Django Shell:

```bash
python manage.py shell
```

Then copy-paste the content from `manual_duplicate_customer_fix.py`

### Rollback Migration (if needed)

If you need to rollback this migration:

```bash
python manage.py migrate app_sales 0009_salesorder_order_source
```

This will revert the unique constraint change (but won't restore deleted duplicates).

## Prevention
Going forward:
- The email field is now unique, preventing duplicate customers with the same email
- The checkout code handles edge cases (empty emails) gracefully

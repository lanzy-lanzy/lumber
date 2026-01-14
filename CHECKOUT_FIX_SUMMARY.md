# Checkout Error Fix - Summary

## The Problem
When trying to checkout from the shopping cart, you get:
```
MultipleObjectsReturned: get() returned more than one Customer -- it returned 2!
```

## Root Cause
- There were duplicate `Customer` records with the same email address in your database
- The checkout endpoint tried to look up the customer by email: `Customer.objects.get(email=...)`
- Django found 2 customers instead of 1, causing the error
- Additionally, `LumberingServiceOrder` has a PROTECT foreign key to Customer, preventing deletion

## The Fix Applied

### 1. Code Changes
**File: `app_sales/models.py`**
- Made the `email` field unique: `email = models.EmailField(blank=True, unique=True, null=True)`

**File: `app_sales/cart_views.py`** (Lines 204-224)
- Added proper handling for customers with missing emails
- Falls back to using customer name if email is empty
- Prevents future similar issues

### 2. Database Migration
**File: `app_sales/migrations/0010_remove_duplicate_customers.py`**
- Identifies all duplicate customers (same email)
- Keeps the oldest customer, marks duplicates for deletion
- **Before deleting**, reassigns all related data:
  - `LumberingServiceOrder` records → kept customer
  - `OrderNotification` records → kept customer
  - `OrderConfirmation` records → kept customer
- Then deletes the duplicate customers
- Adds the unique constraint to prevent future duplicates

## How to Apply the Fix

### Quick Method (Recommended)
```bash
python manage.py migrate
```

The migration handles everything automatically, including reassigning related orders.

### Alternative: Manual Cleanup First
```bash
python manage.py shell < manual_duplicate_customer_fix.py
```

This will:
- Show you all duplicates
- Manually reassign their orders
- Delete the duplicates
- You can then run `python manage.py migrate`

## What This Fixes
✓ Allows checkout to complete successfully
✓ Prevents "MultipleObjectsReturned" errors
✓ Preserves all customer order history
✓ Prevents future duplicate customer issues

## Testing
After applying the fix:
1. Try adding items to the shopping cart
2. Try checking out
3. The order should create successfully

## Files Modified
- `app_sales/models.py` - Added unique constraint to email field
- `app_sales/cart_views.py` - Improved checkout customer handling
- `app_sales/migrations/0010_remove_duplicate_customers.py` - New migration
- `manual_duplicate_customer_fix.py` - Manual cleanup script (optional)
- `CHECKOUT_DUPLICATE_CUSTOMER_FIX.md` - Detailed documentation

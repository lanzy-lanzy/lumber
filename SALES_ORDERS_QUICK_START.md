# Sales Orders - Quick Start Guide

## What Changed?

The Sales Orders page now shows **two separate tables** instead of one mixed list:

### 1. Customer Orders (Purple) 
Orders from authenticated customers shopping from the portal
- **Automatic**: Set when customers checkout from shopping cart
- **Display**: Purple badge and table header

### 2. Point of Sale / Walk-in (Orange)
Orders created by admin for walk-in customers
- **Automatic**: Set when admin creates orders manually
- **Display**: Orange badge and table header

## How to Create an Order

### As Admin (Creates POS/Walk-in Order)
1. Click **"Create Order"** button
2. Search and select a customer (or create new)
3. Select **Payment Type** (Cash, Partial, Credit)
4. Add items to the order
5. Click **"Save Order"**
→ Order automatically marked as **"Point of Sale / Walk-in"**

### As Customer (Creates Customer Order)
1. Login to customer portal
2. Browse and add products to shopping cart
3. Click **"Checkout"**
4. Complete payment
→ Order automatically marked as **"Customer Order"**

## Using Filters

All filters apply to **both tables**:
- **Search**: Find by SO Number or Customer name
- **Payment Type**: Filter by Cash, Partial, or Credit
- **Date Range**: Filter by order date

Example: Search for "gerlan" will show matching orders in both tables.

## Understanding the Summaries

Each table section shows its own statistics:

**Customer Orders Section**:
- Shows stats for all customer portal orders
- Separate totals for Sales, Discounts, Balance

**POS Section**:
- Shows stats for all admin-created orders
- Separate totals for Sales, Discounts, Balance

## Actions Available

Both tables have the same action buttons:
- **👁️ View** - See full order details
- **✏️ Edit** - Modify order (payment type, notes)
- **💳 Record Payment** - Add payment for unpaid orders
- **✓ Mark Ready** - Mark order ready for pickup

## Key Points

✓ **Automatic Assignment** - No need to select order source manually  
✓ **Separate Tracking** - Easy to see portal vs walk-in sales  
✓ **Same Actions** - All features work the same for both types  
✓ **Independent Filters** - Filters apply to both tables  
✓ **Complete History** - All orders (portal + admin) visible  

## Example Workflow

**Walk-in Customer Scenario**:
1. Customer walks in without account
2. Admin clicks "Create Order"
3. Selects customer (walk-in or creates new account)
4. Adds items customer wants
5. Saves with payment type
6. Order appears in **"Point of Sale / Walk-in"** table with **orange** SO Number

**Online Customer Scenario**:
1. Customer logs into portal
2. Browses products
3. Adds to cart
4. Checks out
5. Payment processed
6. Order appears in **"Customer Orders"** table with **purple** SO Number

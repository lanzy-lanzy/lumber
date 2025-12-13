# Shopping Cart - Quick Start Guide

## What Was Implemented
A complete, fully functional shopping cart system that lets customers:
- Browse products
- Add items to cart with quantity selection
- View cart with real-time updates
- Adjust quantities and remove items
- Proceed to checkout and create orders

## How to Use

### For Customers

#### 1. Browse Products
- Go to `/customer/products/`
- Find the product you want

#### 2. Add to Cart
- Click on any product to view details
- Use the +/- buttons to select quantity
- Click "Add to Cart"
- Confirm you want to view the cart (optional)

#### 3. View Shopping Cart
- Click "Shopping Cart" in sidebar or go to `/customer/cart/`
- See all items with images and prices
- Each item shows:
  - Product name and SKU
  - Unit price
  - Quantity controls
  - Subtotal
  - Available stock

#### 4. Manage Cart
- **Increase quantity**: Click + button or type in number
- **Decrease quantity**: Click - button
- **Remove item**: Click "Remove" button
- **Clear entire cart**: Click "Clear Cart" button
- **Continue shopping**: Click "Continue Shopping"

#### 5. Checkout
- Click "Proceed to Checkout" button
- Order is created automatically
- You'll be taken to order details page
- Order number is displayed

### For Admins / Managers

#### View Shopping Carts
1. Go to Django Admin: `/admin/`
2. Navigate to "Shopping Carts" section
3. See all customer carts
4. Click on cart to view items

#### Monitor Cart Items
1. In Admin, go to "Cart Items" section
2. View all items in all carts
3. See unit prices and subtotals
4. Track what customers are looking at

## API Endpoints (for developers)

All endpoints require authentication token.

### Get Cart
```
GET /api/cart/my_cart/
```

### Add Item
```
POST /api/cart/add_item/
Body: {"product_id": 1, "quantity": 5}
```

### Update Item Quantity
```
POST /api/cart/update_item/
Body: {"item_id": 1, "quantity": 10}
```

### Remove Item
```
POST /api/cart/remove_item/
Body: {"item_id": 1}
```

### Clear Cart
```
POST /api/cart/clear_cart/
```

### Checkout (Create Order)
```
POST /api/cart/checkout/
Body: {"payment_type": "partial"}
```

## Key Features

✅ **Stock Validation** - Cannot add more than available
✅ **Real-time Updates** - Cart refreshes automatically
✅ **Product Images** - Shows product photos in cart
✅ **Price Calculation** - Auto-calculates subtotals and totals
✅ **Senior/PWD Support** - Discount notice shown if applicable
✅ **Mobile Friendly** - Works on all screen sizes
✅ **Dark Theme** - Matches existing app design
✅ **Error Messages** - Clear feedback for all actions
✅ **Quick Add** - Easy quantity selection
✅ **Checkout Integration** - Creates sales order automatically

## Testing

### Test Adding Items
1. Login as customer
2. Go to `/customer/products/`
3. Click any product
4. Set quantity to 5
5. Click "Add to Cart"
6. Should see "Added 5 item(s) to cart!"

### Test Cart Page
1. Go to `/customer/cart/`
2. Should see all items you added
3. Try adjusting quantities
4. Cart should update in real-time

### Test Checkout
1. From cart page, click "Proceed to Checkout"
2. Should be redirected to new order page
3. Order number should be displayed
4. Cart should be empty

### Test Stock Validation
1. Note available stock for a product
2. Try to add more than available
3. Should get error message
4. Item won't be added

## Files Changed
- Database: 2 new tables (ShoppingCart, CartItem)
- API: 1 new viewset with 6 endpoints
- Frontend: 1 new cart page, updated product page
- Models: 2 new models with methods
- Serializers: 2 new serializers
- Admin: 2 new admin classes

## Troubleshooting

### Cart is Empty
- Make sure you're logged in
- Refresh the page
- Check that products are marked as "active"

### Can't Add Item
- Check available stock
- Try different quantity
- Refresh and try again

### Checkout Failed
- Ensure cart has items
- Check stock is still available
- Look at browser console for errors

## Navigation

**For Customers:**
- Dashboard → Browse Products → Add to Cart → Shopping Cart → Checkout

**In Sidebar:**
- Dashboard (home)
- Browse Products (product listing)
- Shopping Cart (your cart) **← NEW**
- My Orders (past orders)
- Profile (account info)

## Status
🟢 **FULLY OPERATIONAL**

The shopping cart feature is complete, tested, and ready to use!

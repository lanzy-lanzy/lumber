# Shopping Cart Feature - Complete Implementation Guide

## Overview
The shopping cart feature is now fully operational and allows customers to browse products, add items to cart, manage quantities, and proceed to checkout to create sales orders.

## Features Implemented

### 1. **Database Models** (app_sales/models.py)
- **ShoppingCart**: Stores cart data for each customer user
  - OneToOne relationship with User
  - Methods: `get_total()`, `get_total_items()`, `get_item_count()`, `clear()`
  
- **CartItem**: Individual items in cart
  - ForeignKey to ShoppingCart and LumberProduct
  - Methods: `get_price()`, `get_subtotal()`, `is_in_stock()`
  - Unique constraint on (cart, product)

### 2. **API Endpoints** (app_sales/cart_views.py)
All endpoints require authentication and are accessible at `/api/cart/`

#### GET /api/cart/my_cart/
- Returns current user's shopping cart with all items
- Response includes: items, total, total_items, item_count

#### POST /api/cart/add_item/
- Adds or updates quantity of product in cart
- Payload:
  ```json
  {
    "product_id": 1,
    "quantity": 5
  }
  ```
- Validates stock availability before adding
- Returns updated cart

#### POST /api/cart/update_item/
- Updates quantity of existing cart item
- Payload:
  ```json
  {
    "item_id": 1,
    "quantity": 10
  }
  ```
- Setting quantity to 0 removes the item
- Returns updated cart

#### POST /api/cart/remove_item/
- Removes item from cart
- Payload:
  ```json
  {
    "item_id": 1
  }
  ```
- Returns updated cart

#### POST /api/cart/clear_cart/
- Removes all items from cart
- No payload required
- Returns empty cart

#### POST /api/cart/checkout/
- Creates a sales order from cart items
- Payload:
  ```json
  {
    "payment_type": "partial"  // or "cash", "credit"
  }
  ```
- Automatically creates customer if needed (using user's email)
- Clears cart after successful order creation
- Returns created SalesOrder data

### 3. **Frontend Pages**

#### Product Detail Page (`templates/customer/product_detail.html`)
- Added quantity selector with +/- buttons
- Shows available stock
- "Add to Cart" button with real-time feedback
- Displays confirmation and offers cart redirect

#### Shopping Cart Page (`templates/customer/shopping_cart.html`)
- Displays all cart items with product images
- Quantity controls (number input + -/+ buttons)
- Individual item subtotals
- Cart summary showing:
  - Total items
  - Cart total
  - Senior/PWD discount notice (if applicable)
- Action buttons:
  - Proceed to Checkout
  - Clear Cart
  - Continue Shopping

### 4. **Frontend Views** (core/customer_views.py)
- New view: `customer_shopping_cart()`
- URL: `/customer/cart/`
- Renders shopping cart template with user context

### 5. **Serializers** (app_sales/serializers.py)
- `CartItemSerializer`: Serializes cart items with product details
- `ShoppingCartSerializer`: Serializes complete cart with items and totals

### 6. **Admin Interface** (app_sales/admin.py)
- ShoppingCartAdmin: View all carts, filter by user
- CartItemAdmin: View all cart items, see prices and subtotals

## URL Configuration

### New Routes Added

```python
# In core/urls.py
path('customer/cart/', customer_shopping_cart, name='customer-shopping-cart'),

# In lumber/urls.py
router.register(r'cart', ShoppingCartViewSet, basename='shopping-cart')
```

## Database Migration
Migration file: `app_sales/migrations/0004_shoppingcart_cartitem.py`

Tables created:
- `app_sales_shoppingcart`: Stores cart headers
- `app_sales_cartitem`: Stores cart line items

## Workflow

### Adding to Cart
1. Customer browses products
2. Selects product, adjusts quantity
3. Clicks "Add to Cart"
4. Frontend calls POST `/api/cart/add_item/`
5. Backend validates stock and adds item
6. Cart is updated in real-time
7. Success message shows item count

### Viewing Cart
1. Customer visits `/customer/cart/`
2. Page loads and fetches cart data from API
3. Displays all items with images and prices
4. Auto-refreshes every 5 seconds

### Updating Cart
1. Customer adjusts quantity using +/- buttons or number input
2. Frontend calls POST `/api/cart/update_item/`
3. Cart updates immediately
4. Subtotals recalculate

### Checkout
1. Customer clicks "Proceed to Checkout"
2. Frontend calls POST `/api/cart/checkout/`
3. Backend creates:
   - Customer record (if needed)
   - SalesOrder with items
   - Applies discounts (if senior/PWD)
4. Cart is cleared
5. Customer redirected to order details page

## Features

### Stock Management
- Validates stock before adding items
- Shows available quantity on cart page
- Prevents ordering more than available
- Real-time stock checking

### Pricing
- Displays unit price for each item
- Calculates subtotals per item
- Shows cart total
- Supports pricing by board feet or per piece

### Senior/PWD Discount
- Shows 20% discount notice in cart
- Automatically applied at checkout if customer has flag

### Error Handling
- Stock validation with user-friendly messages
- Invalid quantity handling
- Cart not found handling
- Empty cart checkout prevention

### User Experience
- Smooth animations and transitions
- Loading states for buttons
- Confirmation dialogs for destructive actions
- Real-time cart updates
- Mobile-responsive design
- Dark theme consistent with app

## Testing Endpoints

### Get My Cart
```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/cart/my_cart/
```

### Add Item to Cart
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"product_id": 1, "quantity": 5}' \
  http://localhost:8000/api/cart/add_item/
```

### Checkout
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"payment_type": "partial"}' \
  http://localhost:8000/api/cart/checkout/
```

## Security
- All endpoints require authentication
- CSRF protection enabled
- User can only access their own cart
- Checkout validates stock before creating order

## Performance
- Database queries optimized with select_related()
- Cart auto-refreshes every 5 seconds (configurable)
- Asynchronous API calls prevent page blocking

## Future Enhancements (Optional)
- Wishlist functionality
- Cart persistence (cookie/local storage backup)
- Abandoned cart recovery emails
- Cart sharing with quotes
- Bulk order discounts
- Coupon/promo code support
- Cart recovery after session timeout
- Product recommendations based on cart
- Save cart for later
- Order notes/special instructions

## Troubleshooting

### Cart Items Not Showing
- Clear browser cache
- Check that user is authenticated
- Verify products exist and are active
- Check browser console for JavaScript errors

### Checkout Fails
- Verify stock availability
- Check that customer email is valid
- Ensure payment_type is valid
- Review server logs for validation errors

### Stock Validation Issues
- Verify inventory records exist for products
- Check inventory.quantity_pieces values
- Ensure stock hasn't been reserved elsewhere

## Files Modified/Created

### Created
- app_sales/cart_views.py - Cart API viewset
- templates/customer/shopping_cart.html - Cart page

### Modified
- app_sales/models.py - Added ShoppingCart and CartItem models
- app_sales/serializers.py - Added cart serializers
- app_sales/admin.py - Added cart model admins
- app_sales/migrations/0004_shoppingcart_cartitem.py - Database migration
- lumber/urls.py - Registered cart viewset
- core/urls.py - Added cart route
- core/customer_views.py - Added cart view function
- templates/customer/product_detail.html - Added cart functionality

## Status
✅ COMPLETE AND OPERATIONAL
- Database models created and migrated
- API endpoints fully functional
- Frontend pages created
- Shopping cart operations working
- Checkout integration complete
- Testing verified

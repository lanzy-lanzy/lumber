# Customer Dashboard - Quick Start Guide

## What Was Built

A complete **customer-facing dashboard** with sidebar navigation and product browsing functionality integrated into your Lumber Management System.

## Key Features

### 1. Responsive Sidebar Navigation
- Dashboard
- Browse Products
- My Orders
- Profile
- Logout

### 2. Product Browsing System
- **Browse all active products from database**
- Search by name, SKU, or category
- Filter by lumber category
- Sort by (Newest, Name, Price)
- View detailed product information
- See real-time inventory levels
- View product images (with placeholder fallback)

### 3. Order Management
- View complete order history
- See order totals and balance due
- Check payment status
- View order line items with details
- See customer discounts applied

### 4. Customer Profile
- View personal information
- See delivery address
- Check special status (Senior Citizen, PWD)
- View account statistics

## File Locations

### Backend
```
core/customer_views.py          (NEW - 5 view functions)
core/urls.py                    (MODIFIED - added 5 routes)
```

### Frontend Templates
```
templates/customer/browse_products.html    (NEW - product catalog)
templates/customer/product_detail.html     (NEW - product details)
templates/customer/my_orders.html          (NEW - order history)
templates/customer/order_detail.html       (NEW - order details)
templates/customer/profile.html            (NEW - customer profile)
templates/customer/dashboard.html          (MODIFIED - updated links)
```

## Routes Available

| Route | Purpose |
|-------|---------|
| `/customer/dashboard/` | Main dashboard (existing) |
| `/customer/products/` | Browse products |
| `/customer/products/<id>/` | Product details |
| `/customer/orders/` | Order history |
| `/customer/orders/<id>/` | Order details |
| `/customer/profile/` | Customer profile |

## How to Test

1. **Ensure you're logged in as a customer**
   - Create a customer user account if needed
   - Make sure `is_customer = True` in the user role

2. **Access the customer dashboard**
   ```
   http://localhost:8000/customer/dashboard/
   ```

3. **Click "Browse Products" in the sidebar**
   - Should display all active products from your database
   - Try searching for products
   - Try filtering by category
   - Try sorting by price

4. **View product details**
   - Click on any product card
   - Should show full product details
   - See inventory levels
   - See related products

5. **Check orders**
   - Click "My Orders" in sidebar
   - See order history with summaries
   - Click "View Details" on any order

6. **Visit profile**
   - Click "Profile" in sidebar
   - See all customer information

## Key Technical Details

### Database Models Used
- `LumberProduct` - Product catalog
- `LumberCategory` - Product categories
- `Inventory` - Stock levels
- `SalesOrder` - Order history
- `SalesOrderItem` - Order items
- `Customer` - Customer details
- `CustomUser` - User accounts

### Security
✅ All pages require login (`@login_required`)
✅ Customer-only access verified
✅ Order ownership validated
✅ CSRF protection enabled

### Responsive Design
✅ Mobile-friendly
✅ Tablet-friendly
✅ Desktop-optimized
✅ Dark theme with amber accents

## Customization Options

### Colors
The theme uses:
- Dark slate background: `#0f172a` / `#1e293b`
- Amber accent: `#d97706` / `#fbbf24`
- Status colors: Green (good), Yellow (warning), Red (alert)

To change colors, edit the CSS in template files.

### Product Display
Currently shows:
- Product name, SKU, dimensions
- Price per board foot (and per piece if available)
- Stock quantity and availability status
- Product image

### Search Fields
Currently searches:
- Product name
- SKU
- Category name

### Sort Options
- Newest First (default)
- Name A-Z
- Price Low to High
- Price High to Low

## Future Enhancement Ideas

1. **Shopping Cart**
   - Add items to cart
   - Manage quantities
   - View cart

2. **Checkout**
   - Place orders directly
   - Choose payment method
   - Confirm order

3. **Order Tracking**
   - Track order status
   - View delivery updates
   - See estimated delivery date

4. **Reviews & Ratings**
   - Leave product reviews
   - Rate products
   - See other reviews

5. **Wishlist**
   - Save products for later
   - Compare products
   - Set price alerts

6. **Invoices**
   - Download PDF invoices
   - Email invoices
   - View billing history

7. **Notifications**
   - Order confirmations
   - Shipment updates
   - Back-in-stock alerts

## Troubleshooting

**Products not showing?**
- Check that products exist in database with `is_active=True`
- Check that inventory records exist for products

**Images not loading?**
- Ensure MEDIA_URL is configured
- Check that images are uploaded to media/products/ folder
- Verify file permissions

**Discount not showing?**
- Check customer_profile for is_senior or is_pwd status
- Verify customer is linked to user via email

**Orders not showing?**
- Check that customer records exist in app_sales.Customer
- Verify customer.email matches user.email

## Performance Notes

- Product queries use `select_related()` for efficiency
- Database queries are optimized
- Pagination-ready structure (can add pagination later)
- Image lazy-loading ready

## Support

All views are documented with docstrings.
All templates are well-commented.
See CUSTOMER_DASHBOARD_IMPLEMENTATION.md for detailed documentation.

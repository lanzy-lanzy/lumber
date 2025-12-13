# Customer Dashboard Sidebar & Routes Implementation

## Sidebar Navigation Structure

The customer dashboard sidebar appears on ALL customer pages and provides consistent navigation.

### Navigation Items

```
┌─────────────────────────────────────┐
│   Lumber Pro - Customer Portal      │
├─────────────────────────────────────┤
│  📊 Dashboard                        │ → customer-dashboard
│  🛒 Browse Products                  │ → customer-browse-products
│  📋 My Orders                        │ → customer-my-orders
│  👤 Profile                          │ → customer-profile
├─────────────────────────────────────┤
│  Logged in as: John Doe              │
│  [LOGOUT]                            │
└─────────────────────────────────────┘
```

## Route Mapping

### Dashboard Route
```
Path:     /customer/dashboard/
Name:     customer-dashboard
View:     core.views.customer_dashboard (existing)
Template: templates/customer/dashboard.html (updated)
Auth:     login_required
Role:     customer only
```

### Product Browsing Routes

#### 1. Browse Products (Catalog)
```
Path:     /customer/products/
Name:     customer-browse-products
View:     core.customer_views.customer_browse_products
Template: templates/customer/browse_products.html
Auth:     login_required
Role:     customer only
Features:
  - Display all active products
  - Search functionality
  - Category filtering
  - Sorting options
  - Pagination-ready
Query Parameters:
  - search={query}      (search products)
  - category={id}       (filter by category)
  - sort={field}        (sort by: name, price_per_board_foot, created_at)
```

#### 2. Product Details
```
Path:     /customer/products/<int:product_id>/
Name:     customer-product-detail
View:     core.customer_views.customer_product_detail
Template: templates/customer/product_detail.html
Auth:     login_required
Role:     customer only
Parameters:
  - product_id: The ID of the product to display
Features:
  - Full product information
  - Inventory status
  - Board feet calculations
  - Related products
  - Add to cart button (placeholder)
```

### Order Management Routes

#### 1. My Orders (Order History)
```
Path:     /customer/orders/
Name:     customer-my-orders
View:     core.customer_views.customer_my_orders
Template: templates/customer/my_orders.html
Auth:     login_required
Role:     customer only
Features:
  - List all customer orders
  - Order statistics
  - Status badges
  - Quick view buttons
```

#### 2. Order Details
```
Path:     /customer/orders/<int:order_id>/
Name:     customer-order-detail
View:     core.customer_views.customer_order_detail
Template: templates/customer/order_detail.html
Auth:     login_required
Role:     customer only
Parameters:
  - order_id: The ID of the order to display
Features:
  - Complete order breakdown
  - Line items with prices
  - Payment information
  - Order notes
  - Print functionality
Security:
  - Validates order belongs to customer (by email)
```

### Profile Route

```
Path:     /customer/profile/
Name:     customer-profile
View:     core.customer_views.customer_profile
Template: templates/customer/profile.html
Auth:     login_required
Role:     customer only
Features:
  - Personal information
  - Delivery address
  - Special status indicators
  - Account statistics
```

## Template Navigation Implementation

### All Customer Templates Include Sidebar
```html
<!-- Sidebar Structure (Same on All Pages) -->
<div class="w-64 bg-slate-800">
  <!-- Logo Section -->
  <!-- Navigation Links (with active state highlighting) -->
  <!-- User Info & Logout -->
</div>

<!-- Main Content Area -->
<div class="flex-1">
  <!-- Top Bar with Page Title -->
  <!-- Page-Specific Content -->
  <!-- Footer -->
</div>
```

### Active State Highlighting
The sidebar automatically highlights the current page:
```html
<!-- Example: Browse Products Page -->
<a href="..." class="sidebar-link active">
  <!-- This gets the 'active' class styling -->
</a>
```

## URL Name Usage in Templates

All templates use Django's `{% url %}` template tag for consistency:

```html
<!-- Dashboard -->
<a href="{% url 'customer-dashboard' %}">Dashboard</a>

<!-- Browse Products -->
<a href="{% url 'customer-browse-products' %}">Browse Products</a>

<!-- With Parameters -->
<a href="{% url 'customer-product-detail' product.id %}">View Product</a>
<a href="{% url 'customer-order-detail' order.id %}">View Order</a>

<!-- Orders -->
<a href="{% url 'customer-my-orders' %}">My Orders</a>

<!-- Profile -->
<a href="{% url 'customer-profile' %}">Profile</a>

<!-- Logout -->
<a href="{% url 'logout' %}">Logout</a>
```

## Search & Filter URL Construction

### Search Example
```
/customer/products/?search=hardwood
```

### Category Filter Example
```
/customer/products/?category=5
```

### Sort Example
```
/customer/products/?sort=price_per_board_foot
```

### Combined Example
```
/customer/products/?category=5&search=hardwood&sort=price_per_board_foot
```

## Navigation Flow

```
Customer Login
     ↓
customer-dashboard (default landing)
     ↓
    ├→ customer-browse-products
    │   ├→ customer-product-detail
    │   └→ customer-browse-products (back)
    │
    ├→ customer-my-orders
    │   ├→ customer-order-detail
    │   └→ customer-my-orders (back)
    │
    └→ customer-profile
         └→ customer-browse-products or customer-my-orders (action buttons)
```

## Context Data Passed to Templates

### Browse Products View
```python
{
    'user': request.user,
    'customer_profile': customer_profile,
    'products': products,  # QuerySet of filtered products
    'categories': categories,  # All categories
    'selected_category': category_id,
    'search_query': search_query,
    'sort_by': sort_by,
    'sales_orders': sales_orders[:5],  # Recent orders
    'order_count': order_count,
    'total_spent': total_spent,
}
```

### Product Detail View
```python
{
    'user': request.user,
    'customer_profile': customer_profile,
    'product': product,
    'inventory': inventory,
    'related_products': related_products,  # 4 products from same category
}
```

### My Orders View
```python
{
    'user': request.user,
    'customer_profile': customer_profile,
    'sales_orders': sales_orders,  # All customer orders
    'total_spent': total_spent,
    'order_count': order_count,
}
```

### Order Detail View
```python
{
    'user': request.user,
    'customer_profile': customer_profile,
    'order': sales_order,
    'order_items': order_items,  # Line items
}
```

### Profile View
```python
{
    'user': request.user,
    'customer_profile': customer_profile,
    'order_count': order_count,
    'total_spent': total_spent,
}
```

## View Function Signatures

### customer_browse_products(request)
- GET only
- Requires login
- Requires customer role
- Returns: browse_products.html

### customer_product_detail(request, product_id)
- GET only
- Requires login
- Requires customer role
- Returns: product_detail.html

### customer_my_orders(request)
- GET only
- Requires login
- Requires customer role
- Returns: my_orders.html

### customer_order_detail(request, order_id)
- GET only
- Requires login
- Requires customer role
- Validates order ownership
- Returns: order_detail.html

### customer_profile(request)
- GET only
- Requires login
- Requires customer role
- Returns: profile.html

## Security Checks

1. **Authentication**: All views require `@login_required`
2. **Authorization**: All views check `request.user.is_customer()`
3. **Order Access**: `customer_order_detail()` verifies order belongs to customer

```python
if sales_order.customer.email != request.user.email:
    return redirect('customer-dashboard')
```

## Response Format

All views return rendered HTML templates with full page layouts including:
- Responsive sidebar
- Top navigation bar
- Main content area
- Footer
- Dark theme styling
- Responsive grid layouts

## Performance Optimizations

1. **Database Queries**
   - `select_related('category', 'inventory')` for products
   - Minimized query count
   - Efficient filtering

2. **Template Rendering**
   - Reusable sidebar component
   - Consistent layout structure
   - Optimized CSS selectors

3. **Frontend**
   - CSS-based styling (Tailwind)
   - Minimal JavaScript
   - Responsive design reduces rendering

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Future Route Additions

Potential new routes (not yet implemented):
```
/customer/cart/                    (Shopping cart)
/customer/checkout/                (Order placement)
/customer/wishlist/                (Saved products)
/customer/reviews/                 (Product reviews)
/customer/invoices/                (PDF invoices)
/customer/settings/                (Account settings)
```

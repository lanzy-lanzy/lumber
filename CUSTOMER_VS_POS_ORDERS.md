# Customer Orders vs Point of Sale (POS) / Walk-in Orders

## Overview
The Sales Orders system now automatically distinguishes between two types of orders:

1. **Customer Orders** - Orders placed by authenticated customers through the shopping cart portal
2. **Point of Sale / Walk-in** - Orders manually created by admin staff for walk-in customers

## Automatic Order Source Assignment

### Customer Orders (Automatic)
- **Source**: Customer portal shopping cart checkout
- **Who Creates**: Authenticated customers
- **Order Source Field**: Automatically set to `'customer_order'`
- **Display Badge**: Purple badge with label "Customer Order"
- **Table**: Shown in the "Customer Orders (From Portal)" section

**Flow**:
1. Customer logs in and browses products
2. Adds items to shopping cart
3. Proceeds to checkout
4. Completes payment (cash/partial/credit)
5. Order is created with `order_source='customer_order'` automatically

### Point of Sale / Walk-in (Admin Managed)
- **Source**: Admin manual order creation
- **Who Creates**: Store staff/admin via the admin panel
- **Order Source Field**: Automatically set to `'point_of_sale'`
- **Display Badge**: Orange badge with label "POS / Walk-in"
- **Table**: Shown in the "Point of Sale / Walk-in (Admin Managed)" section

**Flow**:
1. Admin/Staff clicks "Create Order" button
2. Selects customer (walk-in or registered)
3. Adds items to the order
4. Selects payment type
5. Saves order
6. Order is automatically set with `order_source='point_of_sale'`

## User Interface

### Separate Tables
The Sales Orders page now displays **two separate sections**:

#### Section 1: Customer Orders (From Portal)
- **Header Color**: Purple
- **Summary Cards**: Purple-bordered cards
- **Table Header**: Purple background
- **SO Number Color**: Purple text
- **Contains**: All orders placed by customers via portal

#### Section 2: Point of Sale / Walk-in (Admin Managed)
- **Header Color**: Orange
- **Summary Cards**: Orange-bordered cards
- **Table Header**: Orange background
- **SO Number Color**: Orange text
- **Contains**: All orders manually created by admin

### Filters
The search and filter section applies to **both tables**:
- Search by SO Number or Customer name
- Filter by Payment Type (Cash, Partial, Credit)
- Filter by Date Range (Date From, Date To)

Filters apply independently to each table.

### Summary Cards
Each section displays its own statistics:
- **Total Orders** - Count of orders in that category
- **Total Sales** - Sum of total amounts
- **Total Discount** - Sum of discounts applied
- **Pending Balance** - Sum of unpaid balances

## Code Implementation

### Database Model
```python
class SalesOrder(models.Model):
    ORDER_SOURCE_CHOICES = [
        ('customer_order', 'Customer Order'),
        ('point_of_sale', 'Point of Sale / Walk-in'),
    ]
    order_source = models.CharField(
        max_length=20, 
        choices=ORDER_SOURCE_CHOICES, 
        default='point_of_sale'
    )
```

### Service Layer
The `SalesService.create_sales_order()` method accepts an `order_source` parameter:

```python
# For customer checkout (automatic)
so = SalesService.create_sales_order(
    customer_id=customer.id,
    items=items,
    payment_type=payment_type,
    created_by=request.user,
    order_source='customer_order'  # Auto-set for carts
)

# For admin POS orders (automatic)
so = SalesService.create_sales_order(
    customer_id=customer.id,
    items=items,
    payment_type=payment_type,
    created_by=request.user,
    order_source='point_of_sale'  # Auto-set for admin
)
```

### Frontend Logic
JavaScript handles automatic source assignment:
- **Cart checkout** automatically uses `'customer_order'`
- **Admin form submission** automatically sets `'point_of_sale'`
- **Order source field removed** from admin form (no manual selection)

## Benefits

1. **Clear Separation**: Easy to distinguish between portal and walk-in orders
2. **Business Analytics**: Compare revenue from portal vs walk-in customers
3. **Operational Insights**: Track which channel generates more sales
4. **Independent Statistics**: Separate summaries for each order type
5. **Scalability**: Easy to add business logic per order type later

## Migration Notes

- Existing sales orders (created before this update) are set to `'point_of_sale'` by default
- All future orders are automatically categorized
- No manual data cleanup required

## Reporting

To filter orders by source in queries:

```python
# Get customer orders
customer_orders = SalesOrder.objects.filter(order_source='customer_order')

# Get POS orders
pos_orders = SalesOrder.objects.filter(order_source='point_of_sale')
```

## API Response

Orders returned from `/api/sales-orders/` include:
```json
{
    "id": 1,
    "so_number": "SO-20251213-0001",
    "customer": 1,
    "customer_name": "John Doe",
    "order_source": "customer_order",
    "order_source_display": "Customer Order",
    "payment_type": "cash",
    ...
}
```

## Notes

- Order source **cannot be changed** after creation
- The field is read-only in API responses
- Admin form doesn't show or allow selection of order source
- Customer checkout automatically handles source assignment

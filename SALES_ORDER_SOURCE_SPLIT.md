# Sales Order Source Split Implementation

## Overview
The Sales Orders table has been enhanced to identify and distinguish between sales orders coming from **Customer Orders** and **Point of Sale (POS) / Walk-in** transactions.

## Changes Made

### 1. Database Model Update
**File**: `app_sales/models.py`

Added a new field to the `SalesOrder` model:
```python
order_source = models.CharField(
    max_length=20, 
    choices=ORDER_SOURCE_CHOICES, 
    default='point_of_sale'
)
```

**Choices**:
- `customer_order` - Orders placed by customers through the customer portal
- `point_of_sale` - Orders created at the POS system for walk-in customers

### 2. API Serializer Update
**File**: `app_sales/serializers.py`

Updated `SalesOrderSerializer` to include:
- `order_source` - The raw value (for saving)
- `order_source_display` - The human-readable label (for display)

### 3. Database Migration
**File**: `app_sales/migrations/0009_salesorder_order_source.py`

Migration adds the `order_source` field to existing sales orders with a default of `'point_of_sale'`.

### 4. User Interface Updates
**File**: `templates/sales/sales_orders.html`

#### Filter Section
Added a new filter dropdown "Order Source" in the filters section:
- All Sources (default)
- Customer Order (Purple badge)
- Point of Sale / Walk-in (Orange badge)

#### Sales Orders Table
- Added a new column "Order Source" after the Customer column
- Shows color-coded badges:
  - **Purple Badge**: Customer Order
  - **Orange Badge**: POS / Walk-in

#### Create/Edit Order Form
- Added a required "Order Source" dropdown field
- Must be selected before saving an order

#### View Order Modal
- Displays the order source as a colored badge in the order details

### 5. JavaScript Functionality
**Updated Alpine.js functions**:
- `filterOrders()` - Now filters by order source
- `saveOrder()` - Validates and includes order_source in the payload
- `editOrder()` - Populates order_source when loading existing orders
- `closeCreateModal()` - Resets order_source field

## How to Use

### Creating a New Sales Order

1. Click **"Create Order"** button
2. **Select Customer** - Search and select or create a customer
3. **Select Order Source** (new required field):
   - Choose "Customer Order" if the customer placed it through the portal
   - Choose "Point of Sale / Walk-in" for walk-in customers at the store
4. **Select Payment Type** - Cash, Partial Payment, or Credit (SOA)
5. Add items and complete the order
6. Click **"Save Order"**

### Filtering Sales Orders

Use the filters at the top of the table:

1. **Order Source Dropdown**:
   - "All Sources" shows all orders
   - "Customer Order" shows only customer portal orders
   - "Point of Sale / Walk-in" shows only POS/walk-in orders

2. **Combine with other filters** (Search, Payment Type, Date Range) for precise results

### Viewing Order Details

When viewing an order, the Order Source badge is displayed in the order details, making it easy to see at a glance which channel the order came from.

## Default Behavior

- **All existing sales orders** are set to `'point_of_sale'` by default (migration default)
- **All new orders** must explicitly specify an order source
- The field is **required** when creating or editing orders

## Color Scheme

| Source | Color | Badge |
|--------|-------|-------|
| Customer Order | Purple | `bg-purple-100 text-purple-800` |
| POS / Walk-in | Orange | `bg-orange-100 text-orange-800` |

## API Endpoint

**GET/POST** `/api/sales-orders/`

Response includes:
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

## Benefits

1. **Clear Order Tracking** - Know which channel each order came from
2. **Sales Analytics** - Compare customer portal vs POS/walk-in sales
3. **Operational Insights** - Track order sources for business intelligence
4. **Better Organization** - Filter and manage orders by source
5. **Audit Trail** - Keep records of how orders were created

## Notes

- The order source cannot be changed after creation (read-only in API)
- The field is stored but not currently used for auto-routing or notifications
- Future enhancements could include separate dashboards for each order source

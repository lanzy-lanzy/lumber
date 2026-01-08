# Lumbering Service System Implementation

## Overview

The Lumbering Service System is a custom wood milling feature that allows customers to bring their own logs to be cut into lumber. The system records:

- Customer-owned wood intake
- Lumber output with board feet (BF) calculations
- Service fees based on actual output
- Wood shavings ownership tracking
- Simple, direct workflow without approvals

## Features

### 1. Core Components

#### LumberingServiceOrder
Main model for each customer's milling service:
- Customer identification
- Wood input details (type, quantity of logs)
- Service fee configuration (per board foot)
- Shavings ownership assignment
- Order status tracking (Pending → In Progress → Completed)

#### LumberingServiceOutput
Records each lumber batch produced:
- Lumber type/dimensions (2x4, 1x6, etc.)
- Quantity of pieces
- Board feet calculation (automatic)
- Quality grading (Select, Common #1-3)
- Formula: `BF = (Length_ft × Width_in × Thickness_in ÷ 12) × Quantity`

#### ShavingsRecord
Tracks wood shavings (palaras) output:
- Quantity with measurement unit (kg, tons, cubic meters, bags)
- Ownership split (Customer, Company, or 50/50 shared)
- Automatic alignment with order's shavings_ownership setting

### 2. Board Feet Calculation

Board feet is calculated automatically when you add lumber output:

```
Board Feet = (Length in feet × Width in inches × Thickness in inches ÷ 12) × Quantity of pieces
```

**Example:**
- 10 pieces of 2x4 lumber, 12 feet long
- BF = (12 × 4 × 2 ÷ 12) × 10 = 8 × 10 = 80 board feet

### 3. Service Fee Calculation

Total service fee is calculated automatically:

```
Total Service Fee = Total Output Board Feet × Service Fee Per BF
```

**Example:**
- Total output: 500 board feet
- Service fee per BF: ₱5.00
- Total fee: 500 × 5.00 = ₱2,500.00

### 4. Shavings Management

Three ownership options:
- **Customer**: All shavings belong to customer (100% / 0% split)
- **Lumber Company**: All shavings belong to company (0% / 100% split)
- **Shared (50/50)**: Split equally (50% / 50% split)

This is set when creating the service order and auto-applies to all shavings records.

## User Interface

### Admin Dashboard (`/lumbering/`)

**Main Dashboard:**
- Statistics cards (total orders, pending, completed, fees)
- Recent service orders table
- Quick links to create new orders

**Service Orders List (`/lumbering/orders/`):**
- Filterable by status
- Shows customer, wood type, output, fees
- Links to detailed order views

### Order Management

**Create Service Order (`/lumbering/orders/create/`):**
1. Select customer from dropdown
2. Enter wood type (e.g., Mahogany, Pine)
3. Input number of logs received
4. Set service fee per board foot (default ₱5.00)
5. Choose shavings ownership
6. Add optional notes

**Order Detail View (`/lumbering/orders/<id>/`):**
- Shows all order information
- Lists all lumber outputs with board feet calculations
- Shows shavings records with ownership
- Summary cards with totals and fees

**Add Lumber Output (`/lumbering/orders/<id>/outputs/create/`):**
1. Enter lumber type (e.g., "2x4", "1x12")
2. Input quantity of pieces
3. Enter dimensions:
   - Length (feet)
   - Width (inches)
   - Thickness (inches)
4. Board feet auto-calculated
5. Optional: Set quality grade
6. Save - automatically updates service fee

**Record Shavings (`/lumbering/orders/<id>/shavings/create/`):**
1. Enter quantity of shavings
2. Select unit (kg, tons, cubic meters, bags)
3. Ownership automatically set based on order configuration
4. Optional notes
5. Save

### Django Admin Interface

Access at `/admin/lumbering-service/`:

**LumberingServiceOrder Admin:**
- List view with status colors, customer name, output, fees
- Inline editing of outputs and shavings
- Readonly fields for calculated values
- Advanced filters by status, date, ownership

**LumberingServiceOutput Admin:**
- List with dimensions display
- Filter by grade and order
- Calculate board feet automatically

**ShavingsRecord Admin:**
- Show quantity with unit
- Display ownership percentages
- Filter by unit and order

## API Endpoints

### REST API Routes

**Service Orders:**
- `GET /api/lumbering-service-orders/` - List all orders
- `POST /api/lumbering-service-orders/` - Create new order
- `GET /api/lumbering-service-orders/{id}/` - Get order details
- `PATCH /api/lumbering-service-orders/{id}/` - Update order
- `POST /api/lumbering-service-orders/{id}/mark_completed/` - Mark as completed
- `GET /api/lumbering-service-orders/{id}/summary/` - Get order summary

**Service Outputs:**
- `GET /api/lumbering-service-outputs/` - List all outputs
- `POST /api/lumbering-service-outputs/` - Add new output
- `GET /api/lumbering-service-outputs/?order_id=<id>` - Get outputs for specific order

**Shavings Records:**
- `GET /api/shavings-records/` - List all shavings
- `POST /api/shavings-records/` - Record new shavings
- `GET /api/shavings-records/?order_id=<id>` - Get shavings for specific order

## Step-by-Step Usage

### 1. Create a Service Order

```bash
POST /api/lumbering-service-orders/
{
    "customer": 1,
    "wood_type": "Mahogany",
    "quantity_logs": 5,
    "estimated_board_feet": "150.00",
    "service_fee_per_bf": "5.00",
    "shavings_ownership": "lumber_company",
    "notes": "Good quality logs, minimize waste"
}
```

Or use the web form at `/lumbering/orders/create/`

### 2. Add Lumber Output

For each lumber batch produced:

```bash
POST /api/lumbering-service-outputs/
{
    "service_order": 1,
    "lumber_type": "2x4",
    "quantity_pieces": 50,
    "length_feet": "12.00",
    "width_inches": "3.50",
    "thickness_inches": "1.50",
    "grade": "common1",
    "notes": "First batch, clean cuts"
}
```

Board feet automatically calculated:
- BF = (12 × 3.5 × 1.5 ÷ 12) × 50 = 218.75 BF

### 3. Record Shavings

When shavings are collected:

```bash
POST /api/shavings-records/
{
    "service_order": 1,
    "quantity": "850.00",
    "unit": "kg",
    "notes": "Collected from all cuts"
}
```

Ownership automatically set:
- If order is "lumber_company": 0% customer, 100% company
- If order is "customer": 100% customer, 0% company
- If order is "shared": 50% customer, 50% company

### 4. View Order Summary

```bash
GET /api/lumbering-service-orders/1/summary/
```

Returns:
```json
{
    "id": 1,
    "customer": "John Doe",
    "status": "completed",
    "wood_type": "Mahogany",
    "logs": 5,
    "total_board_feet": "1250.50",
    "service_fee_per_bf": "5.00",
    "total_service_fee": "6252.50",
    "output_count": 8,
    "shavings_ownership": "lumber_company"
}
```

## Key Fields & Defaults

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Customer | FK | Required | Select from existing customers |
| Wood Type | CharField | Required | Free-form text (Mahogany, Pine, etc.) |
| Quantity Logs | Integer | Required | Number of logs received |
| Service Fee per BF | Decimal | 5.00 | Customizable per order |
| Shavings Ownership | Choice | lumber_company | Customer / Company / Shared |
| Status | Choice | pending | Auto-set on completion |
| Grade | Choice | common1 | Optional for outputs |

## Workflow Summary

1. **Customer brings logs** → Create Service Order
2. **Start milling process** → Change status to "In Progress"
3. **Produce lumber batches** → Add Lumber Output records (BF auto-calculated)
4. **Collect shavings** → Record Shavings (ownership pre-set)
5. **Complete service** → Mark Order as Completed, finalize fee

## Integration Points

The system integrates with:
- **Customer Management**: Customers from `app_sales.models.Customer`
- **User Management**: Records who created the order
- **Admin Dashboard**: Direct admin interface integration
- **REST API**: Full CRUD operations available

## Database Models

### LumberingServiceOrder
```
- id (PK)
- customer (FK to Customer)
- received_date
- completed_date (nullable)
- status (pending/in_progress/completed/cancelled)
- wood_type (CharField)
- quantity_logs (Integer)
- estimated_board_feet (Decimal)
- service_fee_per_bf (Decimal)
- total_service_fee (Decimal, calculated)
- shavings_ownership (customer/lumber_company/shared)
- notes (TextField)
- created_by (FK to CustomUser)
- created_at (DateTime)
- updated_at (DateTime)
```

### LumberingServiceOutput
```
- id (PK)
- service_order (FK)
- lumber_type (CharField)
- quantity_pieces (Integer)
- length_feet (Decimal)
- width_inches (Decimal)
- thickness_inches (Decimal)
- board_feet (Decimal, auto-calculated)
- grade (CharField: select/common1/common2/common3)
- notes (TextField)
- recorded_at (DateTime)
- updated_at (DateTime)
```

### ShavingsRecord
```
- id (PK)
- service_order (FK)
- quantity (Decimal)
- unit (kg/tons/cubic_meters/bags)
- customer_share (Decimal: 0-100)
- company_share (Decimal: 0-100)
- notes (TextField)
- recorded_at (DateTime)
- updated_at (DateTime)
```

## Admin Sidebar Integration

The Lumbering Service system is accessible from the admin sidebar under:
- **Lumbering Service** → Dashboard
- **Lumbering Service** → Service Orders (List/Create)
- **Django Admin** → Lumbering Service Objects

## Configuration

No additional configuration needed. The system works out of the box with default settings:
- Service fee: ₱5.00 per board foot (customizable per order)
- Shavings ownership: Lumber Company (customizable per order)
- Database: Uses existing SQLite database

## Notes

- All calculations (board feet, service fees) are automatic
- No approval workflow - direct recording for simplicity
- Service fees calculated only after actual output is recorded
- Shavings ownership is pre-set per order, consistent for all shavings
- Customers must exist in system before creating service order
- All fields support editing until order is marked completed

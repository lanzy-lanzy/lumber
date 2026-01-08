# Round Wood Purchasing System - Simplified Version

## Overview

The Round Wood Purchasing system has been completely redesigned as a **simple, single-user system** for direct purchasing of round wood (logs) from suppliers without any approval workflows or complex compliance logic.

## Core Design Philosophy

**Process Flow:** Purchase → Encode Details → Save Record → Update Inventory

- **Single User**: No approval workflows or multi-step authorization
- **Direct Purchasing**: Simple record of what was bought and from whom
- **Fast Data Entry**: Minimal fields, quick encoding
- **Automatic Calculation**: Volume and costs calculated on save
- **Auto Inventory Update**: Completing a purchase automatically updates inventory

## Models

### 1. WoodType
Defines the types of round wood available for purchase.

```python
Fields:
- name: String (unique)
- species: Choice (hardwood, softwood, tropical, mixed)
- description: Text
- default_diameter_inches: Decimal (optional)
- default_length_feet: Decimal (optional)
- is_active: Boolean
```

### 2. RoundWoodPurchase (NEW - Simplified)
**REPLACES** the old multi-step PO workflow. A single record for one purchase from a supplier.

```python
Fields:
- supplier: ForeignKey (Supplier)
- wood_type: ForeignKey (WoodType)
- quantity_logs: Integer (number of logs)
- diameter_inches: Decimal (average log diameter)
- length_feet: Decimal (average log length)
- volume_cubic_feet: Decimal (auto-calculated, readonly)
- unit_cost_per_cubic_foot: Decimal
- total_cost: Decimal (auto-calculated = volume × unit_cost, readonly)
- status: Choice
  - pending: Not yet processed/completed
  - completed: Processed and added to inventory
  - cancelled: Cancelled/voided
- purchase_date: Date
- notes: Text (optional)
- created_by: ForeignKey (CustomUser)
- created_at, updated_at: Timestamps

STATUS FLOW:
pending → completed (mark_completed())
pending → cancelled (cancel)
cancelled → (cannot change)
```

**Key Methods:**
- `calculate_volume()`: Calculates total volume from log specifications
- `save()`: Auto-calculates volume and total_cost before saving
- `mark_completed()`: Marks as completed and updates inventory
- `_update_inventory()`: Adds to RoundWoodInventory

### 3. RoundWoodInventory
Tracks current stock levels by wood type.

```python
Fields:
- wood_type: OneToOneField (WoodType)
- total_logs_in_stock: Integer
- total_cubic_feet_in_stock: Decimal
- total_cost_invested: Decimal
- average_cost_per_cubic_foot: Decimal (auto-calculated)
- warehouse_location: String (optional)
- last_stock_in_date: Date
- last_updated: DateTime (auto)

Auto-populated when:
- RoundWoodPurchase.mark_completed() is called
- Automatically recalculates average cost when new purchases are added
```

## User Interface

### Dashboard (`/round-wood/`)
Summary view with:
- Total purchases count
- Total volume purchased
- Total amount spent
- Pending actions count
- Recent purchases table
- Current inventory summary
- Quick access buttons

### Purchase List (`/round-wood/purchases/`)
Filterable list of all purchases with:
- Filters: Status, Supplier, Wood Type, Search
- Columns: Supplier, Wood Type, Logs, Volume, Cost, Date, Status
- Pagination (20 per page)
- Create new purchase button

### Create Purchase (`/round-wood/purchases/create/`)
Simple form to record a new purchase:

1. **Supplier Information**
   - Select supplier (dropdown)

2. **Wood Details**
   - Wood Type (dropdown)
   - Number of Logs (integer)
   - Diameter (inches) (decimal)
   - Length (feet) (decimal)

3. **Pricing**
   - Unit Cost per Cubic Foot (auto calculates total)
   - (Volume and Total Cost shown as calculated)

4. **Purchase Date**
   - Date of purchase (defaults to today)

5. **Additional Notes** (optional)

**Process Flow Info Box:**
Shows users the step-by-step process and that inventory updates happen automatically when purchase is completed.

### Purchase Detail (`/round-wood/purchases/<id>/`)
Full record view with:
- Supplier information
- Wood details (type, species, dimensions)
- Volume & cost information (all calculated)
- Purchase date and status
- Notes
- Action buttons:
  - "Mark as Completed" (if pending) - adds to inventory
  - "Cancel" (if not completed) - void the purchase

### Inventory List (`/round-wood/inventory/`)
Current stock levels by wood type:
- Summary: Total logs, volume, invested cost
- Table with: Wood Type, Species, Logs, Volume, Avg Cost, Total Cost, Location, Last Updated
- Shows auto-updated inventory from completed purchases

### Wood Types List (`/round-wood/wood-types/`)
Reference list of all wood types with:
- Name, species, description
- Default diameter/length
- Active status

## API Endpoints

### REST API (JSON)

**Base URL:** `/api/round-wood-purchases/`

```
GET     /api/round-wood-purchases/                 # List all purchases
GET     /api/round-wood-purchases/?status=pending  # Filter by status
GET     /api/round-wood-purchases/{id}/            # Get detail
POST    /api/round-wood-purchases/                 # Create new
PATCH   /api/round-wood-purchases/{id}/            # Update
DELETE  /api/round-wood-purchases/{id}/            # Delete (cascade)

# Actions
POST    /api/round-wood-purchases/{id}/complete/   # Mark completed + update inventory
POST    /api/round-wood-purchases/{id}/cancel/     # Cancel purchase

# Summary
GET     /api/round-wood-purchases/summary/         # Get stats
GET     /api/round-wood-purchases/pending/         # Get pending only
```

**Example: Create Purchase**
```json
POST /api/round-wood-purchases/
{
  "supplier": 1,
  "wood_type": 3,
  "quantity_logs": 50,
  "diameter_inches": 12.5,
  "length_feet": 16,
  "unit_cost_per_cubic_foot": 25.00,
  "purchase_date": "2024-12-15",
  "notes": "Delivered to Yard A"
}
```

**Response (auto-calculated fields):**
```json
{
  "id": 1,
  "supplier": 1,
  "supplier_name": "Wood Suppliers Inc",
  "wood_type": 3,
  "wood_type_name": "Oak",
  "quantity_logs": 50,
  "diameter_inches": 12.5,
  "length_feet": 16.0,
  "volume_cubic_feet": 526.18,  # Auto-calculated
  "unit_cost_per_cubic_foot": 25.00,
  "total_cost": 13154.50,  # Auto-calculated
  "status": "pending",
  "purchase_date": "2024-12-15",
  "notes": "Delivered to Yard A",
  "created_by": 2,
  "created_by_name": "John Doe",
  "created_at": "2024-12-15T10:30:00Z",
  "updated_at": "2024-12-15T10:30:00Z"
}
```

## Key Differences from Old System

| Feature | Old System | New System |
|---------|-----------|-----------|
| Model Name | RoundWoodPurchaseOrder | RoundWoodPurchase |
| Workflow | Draft → Ordered → Delivered → Paid | Pending → Completed (or Cancelled) |
| Items Model | RoundWoodPurchaseOrderItem | Direct fields in RoundWoodPurchase |
| Line Items | Multiple items per order | Single wood type per purchase |
| Approvals | Multi-step approval workflow | Single user, no approvals |
| Payment Tracking | Separate payment status | Status is the only state |
| Inspections | Inspection workflow | None |
| Audit Logs | Separate audit log model | Only created_by timestamp |
| Stock Transactions | Separate transactions log | Auto-updated on completion |

## Database Schema

```sql
-- Round Wood Purchase Table
CREATE TABLE app_round_wood_roundwoodpurchase (
  id INTEGER PRIMARY KEY,
  supplier_id INTEGER NOT NULL,
  wood_type_id INTEGER NOT NULL,
  quantity_logs INTEGER NOT NULL,
  diameter_inches DECIMAL(5,2),
  length_feet DECIMAL(5,2),
  volume_cubic_feet DECIMAL(12,2),
  unit_cost_per_cubic_foot DECIMAL(10,2),
  total_cost DECIMAL(14,2),
  status VARCHAR(20),
  purchase_date DATE,
  notes TEXT,
  created_by_id INTEGER,
  created_at DATETIME,
  updated_at DATETIME,
  
  FOREIGN KEY (supplier_id) REFERENCES app_supplier_supplier(id),
  FOREIGN KEY (wood_type_id) REFERENCES app_round_wood_woodtype(id),
  FOREIGN KEY (created_by_id) REFERENCES core_customuser(id),
  
  INDEX supplier_date (supplier_id, purchase_date DESC),
  INDEX status_date (status, purchase_date DESC),
  INDEX wood_type_date (wood_type_id, purchase_date DESC)
);

-- Round Wood Inventory Table (unchanged structure, auto-populated)
CREATE TABLE app_round_wood_roundwoodinventory (
  id INTEGER PRIMARY KEY,
  wood_type_id INTEGER UNIQUE,
  total_logs_in_stock INTEGER,
  total_cubic_feet_in_stock DECIMAL(12,2),
  total_cost_invested DECIMAL(14,2),
  average_cost_per_cubic_foot DECIMAL(10,2),
  warehouse_location VARCHAR(200),
  last_stock_in_date DATE,
  last_updated DATETIME,
  
  FOREIGN KEY (wood_type_id) REFERENCES app_round_wood_woodtype(id)
);
```

## Inventory Auto-Update Flow

1. User creates RoundWoodPurchase with `status='pending'`
2. User views purchase detail and clicks "Mark as Completed"
3. System calls `purchase.mark_completed()`
4. Method changes status to 'completed' and calls `save()`
5. `save()` triggers `_update_inventory()`:
   - Gets or creates RoundWoodInventory for the wood_type
   - Adds logs quantity to total_logs_in_stock
   - Adds volume to total_cubic_feet_in_stock
   - Adds cost to total_cost_invested
   - Recalculates average_cost_per_cubic_foot
   - Updates last_stock_in_date
6. Inventory is now updated

## Validation Rules

**RoundWoodPurchase Creation:**
- Supplier: Required
- Wood Type: Required
- Quantity Logs: Required, minimum 1
- Diameter: Required, greater than 0
- Length: Required, greater than 0
- Unit Cost: Required, non-negative

**Volume Calculation Formula:**
```
Volume (cubic feet) = (π × (diameter_feet/2)² × length_feet × quantity)
where diameter_feet = diameter_inches / 12
```

## Usage Example - Complete Flow

### Via Web UI:

1. Navigate to `/round-wood/purchases/create/`
2. Fill form:
   - Supplier: "ABC Wood Mills"
   - Wood Type: "Oak"
   - Logs: 50
   - Diameter: 12.5 inches
   - Length: 16 feet
   - Cost: ₱25.00/cu ft
   - Date: 2024-12-15
3. Click "Save Purchase"
4. System calculates: Volume ≈ 526.18 cu ft, Total: ₱13,154.50
5. Purchase created with status='pending'
6. View detail page and click "Mark as Completed"
7. Inventory auto-updated with 50 logs, 526.18 cu ft, cost recorded

### Via REST API:

```bash
curl -X POST http://localhost:8000/api/round-wood-purchases/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "supplier": 1,
    "wood_type": 2,
    "quantity_logs": 50,
    "diameter_inches": 12.5,
    "length_feet": 16,
    "unit_cost_per_cubic_foot": 25.00,
    "purchase_date": "2024-12-15",
    "notes": "From Yard A"
  }'

# Mark as completed
curl -X POST http://localhost:8000/api/round-wood-purchases/1/complete/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Migration Notes

**What changed:**
- Old tables: RoundWoodPurchaseOrder, RoundWoodPurchaseOrderItem removed
- New table: RoundWoodPurchase created
- RoundWoodInventory table structure unchanged (data preserved if any existed)

**Data Migration:**
- Old purchase orders cannot be automatically migrated due to structural differences
- Recommendations:
  1. Export old PO data if needed
  2. Let old data be archived
  3. Start fresh with simplified system
  4. Manually enter any critical past purchases if needed

## Files Modified

**Models:**
- `app_round_wood/models.py` - Completely rewritten

**Views:**
- `app_round_wood/views.py` - Updated REST API viewsets
- `app_round_wood/views_ui.py` - Complete UI rewrite for simplified workflow

**Templates:**
- `templates/round_wood/purchase_create.html` - New simplified form
- `templates/round_wood/purchase_list.html` - New purchase list view
- `templates/round_wood/purchase_detail.html` - New detail view
- `templates/round_wood/dashboard.html` - Updated dashboard
- `templates/round_wood/inventory_list.html` - Unchanged structure
- `templates/round_wood/wood_types_list.html` - Reference list

**Serializers:**
- `app_round_wood/serializers.py` - Updated for new model

**Admin:**
- `app_round_wood/admin.py` - Updated for new model

**URLs:**
- `app_round_wood/urls_ui.py` - Updated routes for new views
- `lumber/urls.py` - Updated API route registrations

## Admin Panel

Access via Django admin at `/admin/`:

**RoundWoodPurchase Admin:**
- List: Shows ID, Supplier, Wood Type, Quantity, Volume, Cost, Status, Date
- Filters: Status, Supplier, Wood Type, Purchase Date
- Search: Supplier name, wood type name, notes
- Detail: Full form with auto-calculated fields (readonly)

**RoundWoodInventory Admin:**
- List: Shows Wood Type, Logs, Volume, Avg Cost, Location
- Filters: Wood Type, Last Stock In Date
- Search: Wood type name, location
- Detail: View current levels (all readonly since auto-managed)

## Performance Considerations

- **Indexes:** Created on supplier+date, status+date, wood_type+date for fast filtering
- **Pagination:** 20 items per page on UI
- **Caching:** None (volume calculations are fast)
- **Bulk Operations:** No bulk import/export yet (can be added)

## Future Enhancements

Possible additions (not in initial version):
1. Bulk import purchases from CSV
2. Purchase history by supplier
3. Cost trend analysis
4. Monthly/quarterly reports
5. Budget tracking
6. Supplier performance metrics
7. Automatic reorder suggestions based on inventory levels
8. Barcode scanning for quick entry
9. Mobile app for field entry
10. Multi-location inventory tracking

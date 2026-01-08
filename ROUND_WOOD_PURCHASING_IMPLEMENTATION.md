# Round Wood Purchasing (Goods) Module - Implementation Guide

## Overview

A comprehensive "Round Wood Purchasing (Goods)" module has been implemented for the Lumber and Inventory Management System. This module manages the procurement of round wood (logs) from suppliers, with automatic stock-in, cost tracking, and full ownership transfer management.

## Features Implemented

### 1. **Core Models**

#### WoodType
- Categorizes different types of logs (Hardwood, Softwood, Tropical, Mixed)
- Stores default diameter and length specifications
- Tracks species and descriptions

#### RoundWoodPurchaseOrder
- Main purchase order for round wood
- **Transaction Classification**: Explicitly classified as "round_wood_goods_procurement"
- **Ownership Transfer Tracking**: Monitors ownership transfer status (pending → transferred → confirmed)
- **Status Workflow**:
  - Draft → Submitted → Confirmed → In Transit → Delivered → Inspected → Stocked
- **Key Fields**:
  - PO Number (system-generated)
  - Supplier reference PO number
  - Expected and actual delivery dates
  - Total volume in cubic feet
  - Unit cost per cubic foot
  - Total amount calculation
  - Payment terms tracking

#### RoundWoodPurchaseOrderItem
- Individual batches of logs in each PO
- **Log Specifications**:
  - Quantity of logs
  - Diameter and length measurements
  - Automatic volume calculation using log volume formula
  - Quality grade tracking
- **Inspection Fields**:
  - Inspection status per item
  - Quantity accepted/rejected
  - Detailed inspection notes

#### RoundWoodInventory
- Real-time stock tracking for each wood type
- **Cost Tracking**:
  - Total cost invested
  - Average cost per cubic foot
  - Warehouse location tracking
- Automatic updates when stock is received
- Historical dates for audit trail

#### RoundWoodStockTransaction
- Comprehensive transaction logging
- **Transaction Types**: Stock In, Stock Out, Adjustment, Damage, Waste
- **Reference Tracking**: Links to PO or sales orders
- Cost per unit and total cost tracking
- Created by user audit trail

#### RoundWoodProcurementLog
- Complete audit trail for all procurement activities
- Tracks all status changes with old/new values
- Timestamps and performer identification
- Detailed action logging

### 2. **API Endpoints**

All endpoints accessible at `/api/` prefix:

#### Wood Types
```
GET     /api/wood-types/                 - List all wood types
POST    /api/wood-types/                 - Create new wood type
GET     /api/wood-types/{id}/            - Get specific wood type
PUT     /api/wood-types/{id}/            - Update wood type
DELETE  /api/wood-types/{id}/            - Delete wood type
```

#### Round Wood Purchase Orders
```
GET     /api/round-wood-purchases/                    - List all POs
POST    /api/round-wood-purchases/                    - Create new PO
GET     /api/round-wood-purchases/{id}/               - Get PO details
PUT     /api/round-wood-purchases/{id}/               - Update PO
DELETE  /api/round-wood-purchases/{id}/               - Delete PO

# Custom Actions
POST    /api/round-wood-purchases/{id}/submit/        - Submit for approval
POST    /api/round-wood-purchases/{id}/confirm/       - Confirm/approve order
POST    /api/round-wood-purchases/{id}/mark_delivered/- Mark as delivered
POST    /api/round-wood-purchases/{id}/start_inspection/   - Start inspection
POST    /api/round-wood-purchases/{id}/complete_inspection/- Complete inspection
POST    /api/round-wood-purchases/{id}/stock_in/     - Stock in inventory
POST    /api/round-wood-purchases/{id}/cancel/       - Cancel order

GET     /api/round-wood-purchases/pending_delivery/  - Orders pending delivery
GET     /api/round-wood-purchases/pending_inspection/- Orders pending inspection
GET     /api/round-wood-purchases/summary/           - Summary statistics
```

#### Purchase Order Items
```
GET     /api/round-wood-items/                   - List all items
POST    /api/round-wood-items/                   - Create item
GET     /api/round-wood-items/{id}/              - Get item details
PUT     /api/round-wood-items/{id}/              - Update item
DELETE  /api/round-wood-items/{id}/              - Delete item

POST    /api/round-wood-items/{id}/inspect_item/ - Update inspection status
```

#### Round Wood Inventory
```
GET     /api/round-wood-inventory/              - List inventory
GET     /api/round-wood-inventory/{id}/         - Get inventory details
GET     /api/round-wood-inventory/summary/      - Inventory summary
GET     /api/round-wood-inventory/{id}/valuation/ - Cost valuation
```

#### Stock Transactions
```
GET     /api/round-wood-transactions/          - List transactions
GET     /api/round-wood-transactions/by_wood_type/ - Transactions by type
```

#### Procurement Logs
```
GET     /api/round-wood-logs/                  - List audit logs
```

### 3. **Procurement Workflow**

#### Step 1: Create Purchase Order (Draft)
```python
# Create PO
po = RoundWoodPurchaseOrder.objects.create(
    po_number="RWPO-001",
    supplier=supplier,
    expected_delivery_date="2024-12-25",
    unit_cost_per_cubic_foot=50.00,
    created_by=user
)

# Add items
item = RoundWoodPurchaseOrderItem.objects.create(
    purchase_order=po,
    wood_type=oak_logs,
    quantity_logs=100,
    diameter_inches=12.5,
    length_feet=16.0,
    unit_cost_per_cubic_foot=50.00,
    quality_grade='premium'
)

# Volume calculates automatically
# Volume = π × (diameter/2)² × length × quantity / 12
```

#### Step 2: Submit Order
```python
# Via API: POST /api/round-wood-purchases/{id}/submit/
po.status = 'submitted'
po.save()

# Creates procurement log entry
RoundWoodProcurementLog.objects.create(
    purchase_order=po,
    action='submitted',
    performed_by=user
)
```

#### Step 3: Confirm Order
```python
# Via API: POST /api/round-wood-purchases/{id}/confirm/
po.status = 'confirmed'
po.approved_by=approver
po.save()
```

#### Step 4: Mark Delivered
```python
# Via API: POST /api/round-wood-purchases/{id}/mark_delivered/
# Request body:
{
    "delivery_date": "2024-12-25",
    "delivery_notes": "Delivered in good condition"
}

po.mark_as_delivered(
    delivery_date=delivery_date,
    notes=delivery_notes
)
# Sets: is_delivered=True, status='delivered', ownership_transfer_status='transferred'
```

#### Step 5: Inspection
```python
# Start inspection
# POST /api/round-wood-purchases/{id}/start_inspection/
po.inspection_status = 'in_progress'
po.save()

# Inspect individual items
# POST /api/round-wood-items/{id}/inspect_item/
{
    "status": "passed",
    "quantity_accepted": 98,
    "notes": "2 logs rejected due to cracks"
}

# Complete inspection
# POST /api/round-wood-purchases/{id}/complete_inspection/
{
    "inspector_name": "John Doe",
    "inspection_notes": "All logs meet quality standards",
    "result": "passed"
}
```

#### Step 6: Stock In
```python
# Via API: POST /api/round-wood-purchases/{id}/stock_in/
# Automatically:
# 1. Updates RoundWoodInventory
# 2. Creates RoundWoodStockTransaction records
# 3. Sets ownership_transfer_status = 'confirmed'
# 4. Sets status = 'stocked'

# For each item:
inventory.update_stock(
    quantity_logs=quantity_accepted,
    volume_cubic_feet=item.volume_cubic_feet,
    cost_invested=item.subtotal
)

RoundWoodStockTransaction.objects.create(
    transaction_type='stock_in',
    wood_type=item.wood_type,
    quantity_logs=quantity_accepted,
    volume_cubic_feet=item.volume_cubic_feet,
    cost_per_cubic_foot=item.unit_cost_per_cubic_foot,
    total_cost=item.subtotal,
    reference_type='purchase_order',
    reference_id=po.po_number,
    created_by=user
)
```

### 4. **Ownership Transfer Management**

The system tracks three stages of ownership transfer:

1. **Pending Delivery** (`ownership_transfer_status='pending'`)
   - Order created and confirmed
   - Ownership remains with supplier
   - Not yet in inventory

2. **Transferred** (`ownership_transfer_status='transferred'`)
   - Goods physically delivered
   - Ownership legally transferred to buyer
   - Awaiting inspection

3. **Confirmed** (`ownership_transfer_status='confirmed'`)
   - Inspection completed and passed
   - Stock-in completed
   - Goods in buyer's possession and inventory

### 5. **Cost Tracking System**

#### Per-Item Cost
```python
item.subtotal = item.volume_cubic_feet * unit_cost_per_cubic_foot
```

#### Inventory Valuation
```python
# Total cost invested in this wood type
inventory.total_cost_invested

# Average cost calculation (FIFO/LIFO can be implemented)
inventory.average_cost_per_cubic_foot = (
    total_cost_invested / total_cubic_feet_in_stock
)
```

#### Stock Transaction Tracking
Each stock transaction records:
- Cost per unit at time of transaction
- Total cost
- Reference to purchase order
- Complete audit trail

### 6. **Quality Control & Inspection**

#### Per-Item Inspection
- Status tracking: pending → in_progress → passed/failed/partial
- Quantity acceptance/rejection
- Detailed inspection notes

#### Order-Level Inspection
- Overall inspection status
- Inspector identification
- Inspection date tracking
- Can only stock in if inspection passed

### 7. **Reporting & Analytics**

#### Summary Endpoint
```
GET /api/round-wood-purchases/summary/
Returns:
{
    "total_orders": 10,
    "total_volume_cubic_feet": 5000.0,
    "total_amount": 250000.0,
    "by_status": {...},
    "pending_delivery": 2,
    "pending_inspection": 1
}
```

#### Inventory Summary
```
GET /api/round-wood-inventory/summary/
Returns:
{
    "total_logs_in_stock": 1000,
    "total_cubic_feet_in_stock": 5000.0,
    "total_cost_invested": 250000.0,
    "wood_types_count": 5
}
```

#### Valuation Report
```
GET /api/round-wood-inventory/{id}/valuation/
Returns:
{
    "wood_type": "Oak Logs",
    "quantity_logs": 100,
    "total_cubic_feet": 500.0,
    "total_cost_invested": 25000.0,
    "average_cost_per_cubic_foot": 50.0
}
```

### 8. **Admin Interface**

Full Django admin integration with:
- Purchase order management with inline items
- Inspection tracking with status badges
- Inventory management
- Stock transaction logging
- Procurement audit logs
- Color-coded status indicators
- Bulk actions support

## Database Schema

### Tables Created
1. `app_round_wood_woodtype` - Wood type definitions
2. `app_round_wood_roundwoodpurchaseorder` - Main POs
3. `app_round_wood_roundwoodpurchaseorderitem` - PO line items
4. `app_round_wood_roundwoodinventory` - Stock tracking
5. `app_round_wood_roundwoodstocktransaction` - Stock movements
6. `app_round_wood_roundwoodprocurementlog` - Audit trail

### Indexes
- po_number (for quick lookup)
- status + created_at (for filtering/sorting)
- supplier + created_at (for supplier reports)
- wood_type + created_at (for inventory reports)
- transaction_type + created_at (for transaction reports)

## Integration Points

### With Existing Systems

#### Inventory Module
- Updates `RoundWoodInventory` when stock-in completes
- Creates `RoundWoodStockTransaction` records
- Integrates with overall inventory valuation

#### Supplier Module
- Links to `Supplier` model
- Tracks supplier performance via purchase orders
- Can be included in supplier reports

#### Sales Orders
- Stock-out transactions reference sales orders
- Automatic inventory deduction when logs used
- Can track wood processing history

#### Reporting Module
- Cost analysis by wood type
- Supplier performance metrics
- Inventory turnover rates
- Procurement cycle analysis

## Usage Examples

### Example 1: Create and Process a Purchase Order

```python
from app_round_wood.models import (
    RoundWoodPurchaseOrder,
    RoundWoodPurchaseOrderItem,
    WoodType
)
from app_supplier.models import Supplier
from django.utils import timezone

# Get supplier and wood type
supplier = Supplier.objects.get(company_name="Pine Logs Inc")
oak_logs = WoodType.objects.get(name="Oak Logs")

# Create PO
po = RoundWoodPurchaseOrder.objects.create(
    po_number="RWPO-2024-001",
    supplier=supplier,
    expected_delivery_date="2024-12-25",
    unit_cost_per_cubic_foot=50.00,
    payment_terms="Net 30",
    notes="Premium grade oak logs",
    created_by=request.user
)

# Add item
item = RoundWoodPurchaseOrderItem.objects.create(
    purchase_order=po,
    wood_type=oak_logs,
    quantity_logs=100,
    diameter_inches=12.0,
    length_feet=16.0,
    unit_cost_per_cubic_foot=50.00,
    quality_grade='premium'
)

# Calculate volume (automatically done)
volume = item.calculate_volume()  # Returns cubic feet
item.volume_cubic_feet = volume
item.save()

# Calculate subtotal
item.subtotal = item.calculate_subtotal()
item.save()

# Calculate PO total
po.calculate_total()  # Now total_amount is updated
```

### Example 2: Process Delivery and Inspection

```python
# Mark as delivered
po.mark_as_delivered(
    delivery_date=timezone.now().date(),
    notes="Delivered via truck, all pallets intact"
)

# Start inspection
po.inspection_status = 'in_progress'
po.save()

# Inspect items
item.inspection_status = 'passed'
item.quantity_accepted = 98
item.quantity_rejected = 2
item.inspection_notes = "2 logs had minor cracks, rejected"
item.save()

# Complete inspection
po.mark_inspection_passed(
    inspector_name="John Smith",
    notes="All items meet quality standards except noted rejections"
)
```

### Example 3: Stock In and Track Inventory

```python
# Stock in (automatically creates inventory and transactions)
po.stock_in()

# Now check inventory
from app_round_wood.models import RoundWoodInventory, RoundWoodStockTransaction

inventory = RoundWoodInventory.objects.get(wood_type=oak_logs)
print(f"Stock: {inventory.total_logs_in_stock} logs")
print(f"Volume: {inventory.total_cubic_feet_in_stock} cubic feet")
print(f"Cost: ${inventory.total_cost_invested}")
print(f"Avg Cost/CF: ${inventory.average_cost_per_cubic_foot}")

# Check transactions
transactions = RoundWoodStockTransaction.objects.filter(
    reference_type='purchase_order',
    reference_id='RWPO-2024-001'
)
for txn in transactions:
    print(f"{txn.transaction_type}: {txn.volume_cubic_feet} CF @ ${txn.cost_per_cubic_foot}")
```

## Configuration & Customization

### Add to Settings.py
Already added to INSTALLED_APPS in settings.py:
```python
INSTALLED_APPS = [
    ...
    "app_round_wood",
    ...
]
```

### Register in Admin
Already configured in admin.py with full features:
- Color-coded status badges
- Inline item editing
- Procurement log viewing
- Bulk actions

### Extend Models
To add custom fields:
```python
# Create a migration
python manage.py makemigrations app_round_wood

# Apply it
python manage.py migrate app_round_wood
```

## Best Practices

1. **Always use API endpoints** for creating/updating orders to ensure audit logs are created
2. **Complete inspections** before stocking in to maintain data integrity
3. **Track warehouse locations** for better inventory management
4. **Review procurement logs** for audit trail and troubleshooting
5. **Monitor pending orders** using the dashboard summary
6. **Use payment terms** to track payment obligations
7. **Document rejection reasons** for supplier feedback
8. **Regular inventory reconciliation** with physical counts

## Troubleshooting

### Issue: Stock-in fails
- Ensure inspection status is 'passed'
- Check that RoundWoodInventory exists for the wood type
- Verify quantity_accepted is set for each item

### Issue: Volume calculation incorrect
- Check diameter and length are in correct units (inches/feet)
- Verify formula: π × (diameter/2)² × length × quantity
- Ensure quantity_logs is correct

### Issue: Cost tracking shows wrong average
- Check all transactions have cost_per_cubic_foot
- Verify total_cost = volume × cost_per_unit
- Ensure inventory updates after each stock-in

## Future Enhancements

1. **Batch Processing**: Handle multiple deliveries for single PO
2. **Quality Grades**: Implement quality grade-based pricing
3. **Partial Inspections**: Allow stocking in accepted items while rejecting others
4. **Supplier Rating**: Auto-update supplier ratings based on delivery performance
5. **Notifications**: Email alerts for pending deliveries/inspections
6. **Mobile App**: Mobile interface for on-site inspections
7. **Barcode Scanning**: QR/Barcode for log tracking
8. **Predictive Analytics**: Forecast log usage and optimize orders

## Support & Maintenance

- All models include automatic timestamps (created_at, updated_at)
- Comprehensive indexing for performance
- Audit trail for compliance requirements
- Full permission support via Django auth
- RESTful API for integration with external systems

---

**Status**: ✅ Fully Implemented and Ready for Use
**Version**: 1.0.0
**Last Updated**: 2024

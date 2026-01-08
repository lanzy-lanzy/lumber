# Round Wood Purchasing - Complete API Reference

## Base URL
All endpoints prefixed with: `/api/`

## Authentication
All endpoints require authentication header:
```
Authorization: Bearer {token}
or
Cookie: sessionid={session}
```

---

## Wood Types

### List Wood Types
```http
GET /api/wood-types/
```

**Query Parameters:**
- `species` - Filter by species (hardwood, softwood, tropical, mixed)
- `is_active` - Filter by active status (true/false)
- `search` - Search in name and description
- `page` - Pagination (default: 1)
- `limit` - Items per page (default: 20)

**Response:**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Oak Logs",
            "species": "hardwood",
            "description": "Premium grade oak",
            "default_diameter_inches": 12.0,
            "default_length_feet": 16.0,
            "is_active": true,
            "created_at": "2024-12-01T10:00:00Z",
            "updated_at": "2024-12-01T10:00:00Z"
        }
    ]
}
```

### Create Wood Type
```http
POST /api/wood-types/
Content-Type: application/json

{
    "name": "Pine Logs",
    "species": "softwood",
    "description": "Standard pine logs",
    "default_diameter_inches": 10.0,
    "default_length_feet": 12.0,
    "is_active": true
}
```

**Response:** `201 Created`

### Get Wood Type
```http
GET /api/wood-types/{id}/
```

### Update Wood Type
```http
PUT /api/wood-types/{id}/
PATCH /api/wood-types/{id}/
```

### Delete Wood Type
```http
DELETE /api/wood-types/{id}/
```

---

## Round Wood Purchase Orders

### List Purchase Orders
```http
GET /api/round-wood-purchases/
```

**Query Parameters:**
- `status` - Filter by status (draft, submitted, confirmed, in_transit, delivered, inspected, stocked, cancelled)
- `supplier` - Filter by supplier ID
- `inspection_status` - Filter by inspection status
- `search` - Search in PO number and supplier name
- `ordering` - Sort field (created_at, expected_delivery_date, total_amount)
- `page` - Pagination

**Response:**
```json
{
    "count": 10,
    "results": [
        {
            "id": 1,
            "po_number": "RWPO-2024-001",
            "po_number_supplier": "SUP-001",
            "supplier": 1,
            "supplier_name": "Premium Pine Inc",
            "status": "stocked",
            "order_date": "2024-12-01",
            "expected_delivery_date": "2024-12-25",
            "actual_delivery_date": "2024-12-25",
            "inspection_date": "2024-12-25",
            "total_volume_cubic_feet": "500.00",
            "total_weight_tons": "15.00",
            "unit_cost_per_cubic_foot": "50.00",
            "total_amount": "25000.00",
            "transaction_type": "round_wood_goods_procurement",
            "ownership_transfer_status": "confirmed",
            "is_delivered": true,
            "delivery_notes": "Delivered via truck",
            "inspection_status": "passed",
            "inspection_notes": "All items passed inspection",
            "inspector_name": "John Doe",
            "notes": "Premium grade logs",
            "payment_terms": "Net 30",
            "created_by": 1,
            "created_by_name": "Admin User",
            "approved_by": 1,
            "items": [
                {
                    "id": 1,
                    "purchase_order": 1,
                    "wood_type": 1,
                    "wood_type_name": "Oak Logs",
                    "quantity_logs": 100,
                    "diameter_inches": "12.00",
                    "length_feet": "16.00",
                    "volume_cubic_feet": "500.00",
                    "unit_cost_per_cubic_foot": "50.00",
                    "subtotal": "25000.00",
                    "quality_grade": "premium",
                    "inspection_status": "passed",
                    "inspection_notes": "",
                    "quantity_accepted": 98,
                    "quantity_rejected": 2,
                    "created_at": "2024-12-01T10:00:00Z",
                    "updated_at": "2024-12-01T10:00:00Z"
                }
            ],
            "is_fully_inspected": true,
            "created_at": "2024-12-01T10:00:00Z",
            "updated_at": "2024-12-25T15:00:00Z"
        }
    ]
}
```

### Create Purchase Order
```http
POST /api/round-wood-purchases/
Content-Type: application/json

{
    "po_number": "RWPO-2024-001",
    "po_number_supplier": "SUP-001",
    "supplier": 1,
    "expected_delivery_date": "2024-12-25",
    "unit_cost_per_cubic_foot": 50.00,
    "payment_terms": "Net 30",
    "notes": "Premium grade logs"
}
```

**Response:** `201 Created`

**Automatic Fields Set:**
- `status`: "draft"
- `order_date`: Today
- `transaction_type`: "round_wood_goods_procurement"
- `ownership_transfer_status`: "pending"
- `created_by`: Current user
- `is_delivered`: false
- `inspection_status`: "pending"

### Get Purchase Order
```http
GET /api/round-wood-purchases/{id}/
```

### Update Purchase Order
```http
PUT /api/round-wood-purchases/{id}/
PATCH /api/round-wood-purchases/{id}/
```

### Submit Order
```http
POST /api/round-wood-purchases/{id}/submit/
```

**Status Change:** draft → submitted

**Creates Log Entry:** action="submitted"

**Response:** `200 OK` with updated PO

### Confirm Order
```http
POST /api/round-wood-purchases/{id}/confirm/
```

**Status Change:** submitted → confirmed

**Sets:** `approved_by` = current user

**Creates Log Entry:** action="confirmed"

### Mark Delivered
```http
POST /api/round-wood-purchases/{id}/mark_delivered/
Content-Type: application/json

{
    "delivery_date": "2024-12-25",
    "delivery_notes": "All pallets intact"
}
```

**Status Changes:**
- `status`: confirmed/in_transit → delivered
- `ownership_transfer_status`: pending → transferred
- `is_delivered`: false → true

**Sets:**
- `actual_delivery_date`: provided date
- `delivery_notes`: provided notes

**Creates Log Entry:** action="delivered"

### Start Inspection
```http
POST /api/round-wood-purchases/{id}/start_inspection/
```

**Status Change:** `inspection_status` → "in_progress"

**Requires:** `status` = "delivered"

**Creates Log Entry:** action="inspection_started"

### Complete Inspection
```http
POST /api/round-wood-purchases/{id}/complete_inspection/
Content-Type: application/json

{
    "inspector_name": "John Doe",
    "inspection_notes": "All items passed",
    "result": "passed"
}
```

**Status Changes:**
- `inspection_status`: in_progress → passed/failed
- `status`: delivered → inspected

**Sets:**
- `inspection_date`: Today
- `inspector_name`: Provided name
- `inspection_notes`: Provided notes

**Creates Log Entry:** action="inspection_passed" or "inspection_failed"

### Stock In
```http
POST /api/round-wood-purchases/{id}/stock_in/
```

**Requires:** `inspection_status` = "passed"

**Automatic Actions:**
1. Creates/updates `RoundWoodInventory` for each wood type
2. Creates `RoundWoodStockTransaction` records
3. Updates inventory quantities and costs
4. Calculates average cost per unit

**Status Changes:**
- `status`: inspected → stocked
- `ownership_transfer_status`: transferred → confirmed

**Returns:** Success message with item count

### Cancel Order
```http
POST /api/round-wood-purchases/{id}/cancel/
Content-Type: application/json

{
    "reason": "Supplier unable to deliver on time"
}
```

**Status Change:** → cancelled

**Requires:** Current status not in ["stocked", "received"]

**Creates Log Entry:** action="cancelled"

### Pending Delivery
```http
GET /api/round-wood-purchases/pending_delivery/
```

**Returns:** Orders with status in ["confirmed", "in_transit"]

### Pending Inspection
```http
GET /api/round-wood-purchases/pending_inspection/
```

**Returns:** Orders with status="delivered"

### Summary
```http
GET /api/round-wood-purchases/summary/
```

**Response:**
```json
{
    "total_orders": 10,
    "total_volume_cubic_feet": 5000.0,
    "total_amount": 250000.0,
    "by_status": {
        "draft": 0,
        "submitted": 0,
        "confirmed": 1,
        "in_transit": 0,
        "delivered": 0,
        "inspected": 0,
        "stocked": 9,
        "cancelled": 0
    },
    "pending_delivery": 1,
    "pending_inspection": 0
}
```

---

## Purchase Order Items

### List Items
```http
GET /api/round-wood-items/
```

**Query Parameters:**
- `purchase_order` - Filter by PO ID
- `wood_type` - Filter by wood type ID
- `inspection_status` - Filter by inspection status
- `page` - Pagination

### Create Item
```http
POST /api/round-wood-items/
Content-Type: application/json

{
    "purchase_order": 1,
    "wood_type": 1,
    "quantity_logs": 100,
    "diameter_inches": 12.0,
    "length_feet": 16.0,
    "unit_cost_per_cubic_foot": 50.00,
    "quality_grade": "premium"
}
```

**Automatic Calculations:**
- `volume_cubic_feet`: Calculated using π × (D/2)² × L × Q / 12
- `subtotal`: volume × unit_cost_per_cubic_foot

**Response:** `201 Created` with calculated values

### Get Item
```http
GET /api/round-wood-items/{id}/
```

### Update Item
```http
PUT /api/round-wood-items/{id}/
PATCH /api/round-wood-items/{id}/
```

### Inspect Item
```http
POST /api/round-wood-items/{id}/inspect_item/
Content-Type: application/json

{
    "status": "passed",
    "quantity_accepted": 98,
    "notes": "2 logs rejected due to cracks"
}
```

**Sets:**
- `inspection_status`: provided status
- `quantity_accepted`: provided quantity
- `quantity_rejected`: quantity_logs - quantity_accepted
- `inspection_notes`: provided notes

**Valid Status Values:** pending, in_progress, passed, failed, partial

**Response:** `200 OK` with updated item

### Delete Item
```http
DELETE /api/round-wood-items/{id}/
```

---

## Inventory

### List Inventory
```http
GET /api/round-wood-inventory/
```

**Query Parameters:**
- `wood_type` - Filter by wood type ID

**Response:**
```json
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "wood_type": 1,
            "wood_type_name": "Oak Logs",
            "total_logs_in_stock": 98,
            "total_cubic_feet_in_stock": "490.00",
            "total_cost_invested": "24500.00",
            "average_cost_per_cubic_foot": "50.00",
            "warehouse_location": "Yard A, Section B",
            "last_updated": "2024-12-25T15:00:00Z",
            "last_stock_in_date": "2024-12-25"
        }
    ]
}
```

### Get Inventory
```http
GET /api/round-wood-inventory/{id}/
```

### Inventory Summary
```http
GET /api/round-wood-inventory/summary/
```

**Response:**
```json
{
    "total_logs_in_stock": 500,
    "total_cubic_feet_in_stock": 2500.0,
    "total_cost_invested": 125000.0,
    "wood_types_count": 5
}
```

### Inventory Valuation
```http
GET /api/round-wood-inventory/{id}/valuation/
```

**Response:**
```json
{
    "wood_type": "Oak Logs",
    "quantity_logs": 98,
    "total_cubic_feet": 490.0,
    "total_cost_invested": 24500.0,
    "average_cost_per_cubic_foot": 50.0,
    "warehouse_location": "Yard A, Section B"
}
```

---

## Stock Transactions

### List Transactions
```http
GET /api/round-wood-transactions/
```

**Query Parameters:**
- `transaction_type` - Filter by type (stock_in, stock_out, adjustment, damage, waste)
- `wood_type` - Filter by wood type ID
- `reference_type` - Filter by reference type
- `search` - Search in reference_id or reason
- `ordering` - Sort by created_at or volume_cubic_feet
- `page` - Pagination

**Response:**
```json
{
    "count": 20,
    "results": [
        {
            "id": 1,
            "transaction_type": "stock_in",
            "wood_type": 1,
            "wood_type_name": "Oak Logs",
            "quantity_logs": 98,
            "volume_cubic_feet": "490.00",
            "cost_per_cubic_foot": "50.00",
            "total_cost": "24500.00",
            "reference_type": "purchase_order",
            "reference_id": "RWPO-2024-001",
            "reason": "",
            "created_by": 1,
            "created_by_name": "Admin User",
            "created_at": "2024-12-25T15:00:00Z",
            "notes": "Stocked from PO"
        }
    ]
}
```

### Get Transaction
```http
GET /api/round-wood-transactions/{id}/
```

### By Wood Type
```http
GET /api/round-wood-transactions/by_wood_type/
```

**Response:**
```json
[
    {
        "wood_type__name": "Oak Logs",
        "total_volume": 490.0,
        "total_cost": 24500.0,
        "transaction_count": 1
    }
]
```

---

## Procurement Logs (Audit Trail)

### List Logs
```http
GET /api/round-wood-logs/
```

**Query Parameters:**
- `purchase_order` - Filter by PO ID
- `action` - Filter by action type
- `ordering` - Sort by created_at (default: -created_at)
- `page` - Pagination

**Response:**
```json
{
    "count": 10,
    "results": [
        {
            "id": 1,
            "purchase_order": 1,
            "purchase_order_number": "RWPO-2024-001",
            "action": "created",
            "old_value": "",
            "new_value": "",
            "details": "Round wood purchase order created",
            "performed_by": 1,
            "performed_by_name": "Admin User",
            "created_at": "2024-12-01T10:00:00Z"
        }
    ]
}
```

### Get Log
```http
GET /api/round-wood-logs/{id}/
```

---

## Error Responses

### 400 Bad Request
```json
{
    "error": "Only draft orders can be submitted"
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 500 Server Error
```json
{
    "error": "An unexpected error occurred"
}
```

---

## Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Successful GET or action |
| 201 | Created - Successful POST |
| 204 | No Content - Successful DELETE |
| 400 | Bad Request - Invalid data or operation |
| 401 | Unauthorized - Not authenticated |
| 403 | Forbidden - No permission |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error |

---

## Pagination

Default limit: 20 items per page

```http
GET /api/round-wood-purchases/?page=2&limit=50
```

Response includes:
```json
{
    "count": 100,
    "next": "http://api.example.com/api/round-wood-purchases/?page=3",
    "previous": "http://api.example.com/api/round-wood-purchases/?page=1",
    "results": [...]
}
```

---

## Filtering Examples

### Get Pending Orders
```
GET /api/round-wood-purchases/?status=submitted
```

### Get Orders from Specific Supplier
```
GET /api/round-wood-purchases/?supplier=1
```

### Search by PO Number
```
GET /api/round-wood-purchases/?search=RWPO-2024
```

### Get Failed Inspections
```
GET /api/round-wood-purchases/?inspection_status=failed
```

### Get Orders Needing Delivery
```
GET /api/round-wood-purchases/pending_delivery/
```

---

## Sorting Examples

### Sort by Date (Newest First)
```
GET /api/round-wood-purchases/?ordering=-created_at
```

### Sort by Amount (Highest First)
```
GET /api/round-wood-purchases/?ordering=-total_amount
```

### Sort by Delivery Date
```
GET /api/round-wood-purchases/?ordering=expected_delivery_date
```

---

**Last Updated:** 2024
**Version:** 1.0.0

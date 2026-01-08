# Lumbering Service - API Examples

## Complete Workflow Example

This document shows a complete lumbering service workflow using the REST API.

## 1. Create a Service Order

**Endpoint:** `POST /api/lumbering-service-orders/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/lumbering-service-orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer": 1,
    "wood_type": "Mahogany",
    "quantity_logs": 5,
    "estimated_board_feet": "150.00",
    "service_fee_per_bf": "5.00",
    "shavings_ownership": "lumber_company",
    "notes": "High quality logs, minimize waste"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "customer": 1,
  "customer_name": "John Doe",
  "received_date": "2025-01-15",
  "completed_date": null,
  "status": "pending",
  "wood_type": "Mahogany",
  "quantity_logs": 5,
  "estimated_board_feet": "150.00",
  "service_fee_per_bf": "5.00",
  "total_service_fee": null,
  "shavings_ownership": "lumber_company",
  "actual_output_bf": 0,
  "outputs": [],
  "shavings": [],
  "notes": "High quality logs, minimize waste",
  "created_by": 1,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

**Key Notes:**
- `id` is auto-generated (1 in this example)
- `actual_output_bf` is 0 because no outputs yet
- `total_service_fee` is null until outputs are added
- `status` defaults to "pending"
- `created_by` is auto-filled from authenticated user

---

## 2. Add First Lumber Output

**Endpoint:** `POST /api/lumbering-service-outputs/`

Customer milled 50 pieces of 2×4 lumber, 12 feet long.

**Request:**
```bash
curl -X POST http://localhost:8000/api/lumbering-service-outputs/ \
  -H "Content-Type: application/json" \
  -d '{
    "service_order": 1,
    "lumber_type": "2x4",
    "quantity_pieces": 50,
    "length_feet": "12.00",
    "width_inches": "3.50",
    "thickness_inches": "1.50",
    "grade": "common1",
    "notes": "Clean cuts, first batch"
  }'
```

**Calculation:**
```
BF = (12 × 3.5 × 1.5 ÷ 12) × 50
   = (5.25) × 50
   = 262.50 board feet
```

**Response (201 Created):**
```json
{
  "id": 1,
  "service_order": 1,
  "lumber_type": "2x4",
  "quantity_pieces": 50,
  "length_feet": "12.00",
  "width_inches": "3.50",
  "thickness_inches": "1.50",
  "board_feet": "262.50",
  "grade": "common1",
  "notes": "Clean cuts, first batch",
  "recorded_at": "2025-01-15T10:35:00Z",
  "updated_at": "2025-01-15T10:35:00Z"
}
```

**Key Notes:**
- Board feet calculated automatically: 262.50 BF
- Service order's `total_service_fee` is now: 262.50 × 5.00 = ₱1,312.50

---

## 3. Add More Lumber Output

Customer continues milling. Second batch: 1×12 boards.

**Request:**
```bash
curl -X POST http://localhost:8000/api/lumbering-service-outputs/ \
  -H "Content-Type: application/json" \
  -d '{
    "service_order": 1,
    "lumber_type": "1x12",
    "quantity_pieces": 30,
    "length_feet": "10.00",
    "width_inches": "11.50",
    "thickness_inches": "0.75",
    "grade": "common1",
    "notes": "Good quality boards"
  }'
```

**Calculation:**
```
BF = (10 × 11.5 × 0.75 ÷ 12) × 30
   = (7.1875) × 30
   = 215.625 board feet
```

**Response (201 Created):**
```json
{
  "id": 2,
  "service_order": 1,
  "lumber_type": "1x12",
  "quantity_pieces": 30,
  "length_feet": "10.00",
  "width_inches": "11.50",
  "thickness_inches": "0.75",
  "board_feet": "215.625",
  "grade": "common1",
  "notes": "Good quality boards",
  "recorded_at": "2025-01-15T11:00:00Z",
  "updated_at": "2025-01-15T11:00:00Z"
}
```

**Updated Order Total:**
- Total BF: 262.50 + 215.625 = 478.125 BF
- Total Fee: 478.125 × 5.00 = ₱2,390.63

---

## 4. Add Third Output

One more batch of 4×4 posts.

**Request:**
```bash
curl -X POST http://localhost:8000/api/lumbering-service-outputs/ \
  -H "Content-Type: application/json" \
  -d '{
    "service_order": 1,
    "lumber_type": "4x4",
    "quantity_pieces": 20,
    "length_feet": "8.00",
    "width_inches": "3.75",
    "thickness_inches": "3.75",
    "grade": "select",
    "notes": "Premium grade posts"
  }'
```

**Calculation:**
```
BF = (8 × 3.75 × 3.75 ÷ 12) × 20
   = (9.375) × 20
   = 187.50 board feet
```

**Updated Order Total:**
- Total BF: 262.50 + 215.625 + 187.50 = 665.625 BF
- Total Fee: 665.625 × 5.00 = ₱3,328.13

---

## 5. Record Wood Shavings (Palaras)

The milling produced wood shavings. Company owns them.

**Endpoint:** `POST /api/shavings-records/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/shavings-records/ \
  -H "Content-Type: application/json" \
  -d '{
    "service_order": 1,
    "quantity": "1200.50",
    "unit": "kg",
    "notes": "Collected from all three batches"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "service_order": 1,
  "quantity": "1200.50",
  "unit": "kg",
  "customer_share": "0.00",
  "company_share": "100.00",
  "notes": "Collected from all three batches",
  "recorded_at": "2025-01-15T12:00:00Z",
  "updated_at": "2025-01-15T12:00:00Z"
}
```

**Key Notes:**
- `customer_share`: 0% (order has `shavings_ownership: "lumber_company"`)
- `company_share`: 100% (auto-set from order)
- Ownership is automatically set, no manual entry needed

---

## 6. Get Order Summary

**Endpoint:** `GET /api/lumbering-service-orders/1/summary/`

**Request:**
```bash
curl http://localhost:8000/api/lumbering-service-orders/1/summary/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "customer": "John Doe",
  "status": "pending",
  "wood_type": "Mahogany",
  "logs": 5,
  "total_board_feet": "665.625",
  "service_fee_per_bf": "5.00",
  "total_service_fee": "3328.13",
  "output_count": 3,
  "shavings_ownership": "lumber_company"
}
```

---

## 7. Get Full Order Details

**Endpoint:** `GET /api/lumbering-service-orders/1/`

**Request:**
```bash
curl http://localhost:8000/api/lumbering-service-orders/1/
```

**Response:**
```json
{
  "id": 1,
  "customer": 1,
  "customer_name": "John Doe",
  "received_date": "2025-01-15",
  "completed_date": null,
  "status": "pending",
  "wood_type": "Mahogany",
  "quantity_logs": 5,
  "estimated_board_feet": "150.00",
  "service_fee_per_bf": "5.00",
  "total_service_fee": "3328.13",
  "shavings_ownership": "lumber_company",
  "actual_output_bf": "665.625",
  "outputs": [
    {
      "id": 1,
      "service_order": 1,
      "lumber_type": "2x4",
      "quantity_pieces": 50,
      "length_feet": "12.00",
      "width_inches": "3.50",
      "thickness_inches": "1.50",
      "board_feet": "262.50",
      "grade": "common1",
      "notes": "Clean cuts, first batch",
      "recorded_at": "2025-01-15T10:35:00Z",
      "updated_at": "2025-01-15T10:35:00Z"
    },
    {
      "id": 2,
      "service_order": 1,
      "lumber_type": "1x12",
      "quantity_pieces": 30,
      "length_feet": "10.00",
      "width_inches": "11.50",
      "thickness_inches": "0.75",
      "board_feet": "215.625",
      "grade": "common1",
      "notes": "Good quality boards",
      "recorded_at": "2025-01-15T11:00:00Z",
      "updated_at": "2025-01-15T11:00:00Z"
    },
    {
      "id": 3,
      "service_order": 1,
      "lumber_type": "4x4",
      "quantity_pieces": 20,
      "length_feet": "8.00",
      "width_inches": "3.75",
      "thickness_inches": "3.75",
      "board_feet": "187.50",
      "grade": "select",
      "notes": "Premium grade posts",
      "recorded_at": "2025-01-15T12:00:00Z",
      "updated_at": "2025-01-15T12:00:00Z"
    }
  ],
  "shavings": [
    {
      "id": 1,
      "service_order": 1,
      "quantity": "1200.50",
      "unit": "kg",
      "customer_share": "0.00",
      "company_share": "100.00",
      "notes": "Collected from all three batches",
      "recorded_at": "2025-01-15T12:00:00Z",
      "updated_at": "2025-01-15T12:00:00Z"
    }
  ],
  "notes": "High quality logs, minimize waste",
  "created_by": 1,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T12:00:00Z"
}
```

---

## 8. Mark Order as Completed

**Endpoint:** `POST /api/lumbering-service-orders/1/mark_completed/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/lumbering-service-orders/1/mark_completed/
```

**Response:**
```json
{
  "status": "Order marked as completed"
}
```

**Effects:**
- `status` changes to "completed"
- `completed_date` set to today
- Order locked (can't edit status further)

---

## 9. Get Outputs for Specific Order

**Endpoint:** `GET /api/lumbering-service-outputs/?order_id=1`

**Request:**
```bash
curl "http://localhost:8000/api/lumbering-service-outputs/?order_id=1"
```

**Response:**
```json
[
  {
    "id": 1,
    "service_order": 1,
    "lumber_type": "2x4",
    "quantity_pieces": 50,
    "length_feet": "12.00",
    "width_inches": "3.50",
    "thickness_inches": "1.50",
    "board_feet": "262.50",
    "grade": "common1",
    "notes": "Clean cuts, first batch",
    "recorded_at": "2025-01-15T10:35:00Z",
    "updated_at": "2025-01-15T10:35:00Z"
  },
  {
    "id": 2,
    "service_order": 1,
    "lumber_type": "1x12",
    "quantity_pieces": 30,
    "length_feet": "10.00",
    "width_inches": "11.50",
    "thickness_inches": "0.75",
    "board_feet": "215.625",
    "grade": "common1",
    "notes": "Good quality boards",
    "recorded_at": "2025-01-15T11:00:00Z",
    "updated_at": "2025-01-15T11:00:00Z"
  },
  {
    "id": 3,
    "service_order": 1,
    "lumber_type": "4x4",
    "quantity_pieces": 20,
    "length_feet": "8.00",
    "width_inches": "3.75",
    "thickness_inches": "3.75",
    "board_feet": "187.50",
    "grade": "select",
    "notes": "Premium grade posts",
    "recorded_at": "2025-01-15T12:00:00Z",
    "updated_at": "2025-01-15T12:00:00Z"
  }
]
```

---

## 10. Get Shavings for Specific Order

**Endpoint:** `GET /api/shavings-records/?order_id=1`

**Request:**
```bash
curl "http://localhost:8000/api/shavings-records/?order_id=1"
```

**Response:**
```json
[
  {
    "id": 1,
    "service_order": 1,
    "quantity": "1200.50",
    "unit": "kg",
    "customer_share": "0.00",
    "company_share": "100.00",
    "notes": "Collected from all three batches",
    "recorded_at": "2025-01-15T12:00:00Z",
    "updated_at": "2025-01-15T12:00:00Z"
  }
]
```

---

## Common Scenarios

### Scenario 1: Customer Takes Shavings

**Setup:** Customer gets all shavings

**When creating order:**
```json
{
  "customer": 1,
  "wood_type": "Pine",
  "quantity_logs": 3,
  "service_fee_per_bf": "4.50",
  "shavings_ownership": "customer"
}
```

**When recording shavings:**
- `customer_share`: 100%
- `company_share`: 0%

---

### Scenario 2: Split Shavings

**Setup:** Customer and company split 50/50

**When creating order:**
```json
{
  "customer": 1,
  "wood_type": "Oak",
  "quantity_logs": 4,
  "service_fee_per_bf": "6.00",
  "shavings_ownership": "shared"
}
```

**When recording shavings:**
- `customer_share`: 50%
- `company_share`: 50%

---

### Scenario 3: Multiple Shavings Batches

Record shavings multiple times as they're collected:

**First batch:**
```bash
POST /api/shavings-records/
{
  "service_order": 1,
  "quantity": "500",
  "unit": "kg",
  "notes": "First day collection"
}
```

**Second batch (next day):**
```bash
POST /api/shavings-records/
{
  "service_order": 1,
  "quantity": "650",
  "unit": "kg",
  "notes": "Second day collection"
}
```

Both records appear in `GET /api/shavings-records/?order_id=1`

---

## Error Examples

### Invalid Service Fee (negative)

**Request:**
```bash
POST /api/lumbering-service-outputs/
{
  "service_order": 1,
  "lumber_type": "2x4",
  "quantity_pieces": 50,
  "length_feet": "-12.00",
  "width_inches": "3.50",
  "thickness_inches": "1.50"
}
```

**Response (400 Bad Request):**
```json
{
  "length_feet": [
    "Ensure this value is greater than or equal to 0.01."
  ]
}
```

### Missing Required Field

**Request:**
```bash
POST /api/lumbering-service-orders/
{
  "customer": 1,
  "wood_type": "Mahogany"
  // missing quantity_logs
}
```

**Response (400 Bad Request):**
```json
{
  "quantity_logs": [
    "This field is required."
  ]
}
```

### Customer Not Found

**Request:**
```bash
POST /api/lumbering-service-orders/
{
  "customer": 99999,  // doesn't exist
  "wood_type": "Oak",
  "quantity_logs": 5,
  "service_fee_per_bf": "5.00",
  "shavings_ownership": "lumber_company"
}
```

**Response (400 Bad Request):**
```json
{
  "customer": [
    "Invalid pk \"99999\" - object does not exist."
  ]
}
```

---

## Quick Calculation Reference

### Board Feet Examples

| Lumber | Qty | Length | Width | Thick | Formula | Result |
|--------|-----|--------|-------|-------|---------|--------|
| 2×4 | 50 | 12' | 3.5" | 1.5" | (12×3.5×1.5÷12)×50 | 262.50 |
| 1×12 | 30 | 10' | 11.5" | 0.75" | (10×11.5×0.75÷12)×30 | 215.63 |
| 4×4 | 20 | 8' | 3.75" | 3.75" | (8×3.75×3.75÷12)×20 | 187.50 |
| 2×6 | 40 | 14' | 5.5" | 1.5" | (14×5.5×1.5÷12)×40 | 385.00 |

### Service Fee Examples

| Total BF | Fee/BF | Total Fee |
|----------|--------|-----------|
| 500 | ₱5.00 | ₱2,500 |
| 665.63 | ₱5.00 | ₱3,328.13 |
| 1,000 | ₱6.00 | ₱6,000 |
| 1,500 | ₱4.50 | ₱6,750 |

---

## Testing with Postman/cURL

All examples are ready to use with cURL or Postman. Import the endpoints into your API tool and test the workflow.

**Auth Note:** If your API requires authentication, add:
```bash
-H "Authorization: Bearer YOUR_TOKEN"
```

or 

```bash
-H "Authorization: Token YOUR_TOKEN"
```

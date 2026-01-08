# Round Wood System - Quick Start Guide

## What Changed?

The old complex Purchase Order system with multiple steps (Draft → Ordered → Delivered → Paid) has been replaced with a **simple, direct purchase recording system**:

**New Process:** Purchase → Encode Details → Save Record → Update Inventory

## Quick Navigation

### For Users

**Web Interface:**
- Dashboard: `/round-wood/`
- New Purchase: `/round-wood/purchases/create/`
- All Purchases: `/round-wood/purchases/`
- Inventory: `/round-wood/inventory/`
- Wood Types: `/round-wood/wood-types/`

### For Developers

**API Base:** `/api/round-wood-purchases/`
**Models:** `RoundWoodPurchase` (replaces `RoundWoodPurchaseOrder`)

## Recording a Purchase

### Option 1: Web Form (Easiest)

1. Go to `/round-wood/purchases/create/`
2. Fill in:
   - **Supplier**: Who sold the logs
   - **Wood Type**: Type of wood purchased
   - **Number of Logs**: How many logs
   - **Diameter (inches)**: Average log thickness
   - **Length (feet)**: Average log length
   - **Cost per Cubic Foot**: Price per cu ft
   - **Date**: When purchased
   - **Notes**: Any additional info
3. Click "Save Purchase"
4. Volume and total cost auto-calculated
5. Purchase created with status "Pending"
6. Click "Mark as Completed" to add to inventory

### Option 2: REST API

```bash
POST /api/round-wood-purchases/
{
  "supplier": 1,
  "wood_type": 2,
  "quantity_logs": 50,
  "diameter_inches": 12.5,
  "length_feet": 16,
  "unit_cost_per_cubic_foot": 25.00,
  "purchase_date": "2024-12-15"
}

# Then complete it:
POST /api/round-wood-purchases/1/complete/
```

## Status Flow

```
┌─────────────────────────────────────────────┐
│  Create Purchase (status = "pending")       │
├─────────────────────────────────────────────┤
│  Review Details                             │
└─────────────────────────────────────────────┘
         ↓
    Two Options:
    ↙           ↘
┌───────────┐  ┌──────────────┐
│ Complete  │  │    Cancel    │
│ (Add to   │  │   (Void)     │
│ Inventory)│  │              │
└───────────┘  └──────────────┘
```

## Key Fields

| Field | What It Does | Notes |
|-------|-------------|-------|
| Supplier | Who you're buying from | Required dropdown |
| Wood Type | Type of wood (Oak, Pine, etc) | Required dropdown |
| Quantity | Number of logs | Required, min 1 |
| Diameter | Width of log in inches | Required, > 0 |
| Length | Length in feet | Required, > 0 |
| Unit Cost | Cost per cubic foot (₱) | Required |
| Volume | CALCULATED - don't enter | Auto-computed from dimensions |
| Total Cost | CALCULATED - don't enter | Auto-computed: volume × unit_cost |

## Inventory Auto-Update

**When:** After you mark a purchase as "Completed"

**What Happens:**
1. Purchase status → "Completed"
2. System calculates volume from dimensions
3. System adds to RoundWoodInventory:
   - Adds quantity_logs
   - Adds volume (cubic feet)
   - Adds cost
   - Updates average cost per cubic foot
4. **No manual inventory entry needed!**

## Viewing Data

### List All Purchases
- `/round-wood/purchases/` - Web interface
- `/api/round-wood-purchases/` - API

### Filter Purchases
- By Status: pending, completed, cancelled
- By Supplier: dropdown
- By Wood Type: dropdown
- By Date range: coming soon
- By search text: supplier name, notes

### View One Purchase
- Click "View" on list
- Or: `/round-wood/purchases/{id}/`
- Or API: `/api/round-wood-purchases/{id}/`

### Check Inventory
- `/round-wood/inventory/` - Current stock by wood type

## Common Tasks

### Add a Log Purchase
1. `/round-wood/purchases/create/`
2. Fill form → Save
3. Click "Mark as Completed"
4. Done! Inventory auto-updated

### Cancel a Purchase
1. Go to purchase detail
2. Click "Cancel Purchase"
3. Purchase voided (won't add to inventory)

### See How Much We Spent
1. `/round-wood/purchases/`
2. Look at "Total Cost" column
3. Or API: `/api/round-wood-purchases/summary/`

### Check Current Stock
1. `/round-wood/inventory/`
2. See all wood types and quantities
3. Shows total cost invested per type

### View Pending Actions
1. Dashboard: `/round-wood/`
2. "Pending Actions" card shows count
3. Click links to process them

## Models Reference

### RoundWoodPurchase
Single record = one purchase from supplier

```
Fields:
- id: Auto
- supplier: Link to supplier
- wood_type: Link to wood type
- quantity_logs: Number (50, 100, etc)
- diameter_inches: Decimal (12.5)
- length_feet: Decimal (16.0)
- volume_cubic_feet: CALCULATED
- unit_cost_per_cubic_foot: Decimal (25.00)
- total_cost: CALCULATED
- status: pending, completed, cancelled
- purchase_date: Date
- notes: Optional text
- created_by: User who created it
- created_at, updated_at: Timestamps
```

### RoundWoodInventory
Current stock levels (auto-managed)

```
Fields:
- wood_type: Which wood type
- total_logs_in_stock: Number
- total_cubic_feet_in_stock: Volume
- total_cost_invested: Total ₱ spent
- average_cost_per_cubic_foot: Calculated
- warehouse_location: Optional location
- last_stock_in_date: Last purchase date
- last_updated: Timestamp
```

## API Examples

### Create Purchase
```bash
curl -X POST http://localhost:8000/api/round-wood-purchases/ \
  -H "Authorization: Token ABC123" \
  -H "Content-Type: application/json" \
  -d '{
    "supplier": 1,
    "wood_type": 2,
    "quantity_logs": 50,
    "diameter_inches": 12.5,
    "length_feet": 16,
    "unit_cost_per_cubic_foot": 25.00,
    "purchase_date": "2024-12-15",
    "notes": "From Mill A"
  }'
```

### Get All Pending
```bash
curl http://localhost:8000/api/round-wood-purchases/pending/ \
  -H "Authorization: Token ABC123"
```

### Complete a Purchase
```bash
curl -X POST http://localhost:8000/api/round-wood-purchases/1/complete/ \
  -H "Authorization: Token ABC123"
```

### Get Summary
```bash
curl http://localhost:8000/api/round-wood-purchases/summary/ \
  -H "Authorization: Token ABC123"
```

### Filter by Status
```bash
curl http://localhost:8000/api/round-wood-purchases/?status=pending \
  -H "Authorization: Token ABC123"
```

## Troubleshooting

**Volume shows as 0:**
- Check that diameter and length are entered correctly
- Both must be > 0
- Saved automatically on form submission

**Inventory not updating:**
- Make sure purchase status is "Completed"
- Check that wood_type exists
- Check django logs for errors

**Can't find a purchase:**
- Use filters on `/round-wood/purchases/`
- Search by supplier name or notes
- Check status (pending/completed/cancelled)

**Getting permission errors:**
- Make sure you're logged in
- Check that user has permission to create/edit
- Admin can adjust permissions in Django admin

## Files Overview

**Models:**
- `app_round_wood/models.py` - RoundWoodPurchase, RoundWoodInventory, WoodType

**Views:**
- `app_round_wood/views_ui.py` - Web interface views
- `app_round_wood/views.py` - REST API viewsets

**Templates:**
- `templates/round_wood/purchase_create.html` - New purchase form
- `templates/round_wood/purchase_detail.html` - View/edit purchase
- `templates/round_wood/purchase_list.html` - List all purchases
- `templates/round_wood/dashboard.html` - Dashboard
- `templates/round_wood/inventory_list.html` - Inventory view

**URLs:**
- `app_round_wood/urls_ui.py` - Web routes
- Routes in `/api/round-wood-purchases/` for API

## Database Tables

**Old (Removed):**
- app_round_wood_roundwoodpurchaseorder
- app_round_wood_roundwoodpurchaseorderitem

**New:**
- app_round_wood_roundwoodpurchase

**Unchanged:**
- app_round_wood_woodtype
- app_round_wood_roundwoodinventory

## Next Steps

1. **Test it out**: Create a purchase and mark it completed
2. **Check inventory**: See if it updated correctly
3. **Try the API**: Use REST endpoints if you use them
4. **Bulk upload**: Can add CSV import feature if needed
5. **Reports**: Can add monthly summaries if needed

## Need Help?

- Check purchase detail page - shows calculation
- Look at inventory - shows auto-updated totals
- Review API docs in `/api/`
- Check admin interface: `/admin/app_round_wood/`

---

**Version:** Simplified (2024-12-15)
**Process:** Purchase → Encode → Save → Auto-Update Inventory

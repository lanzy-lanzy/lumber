# Round Wood Purchasing System

## Overview

The Round Wood Purchasing system is now a **simple, streamlined solution for direct wood purchasing and inventory management**. Designed for single users who are both the buyer and decision-maker.

**Process:** Purchase → Encode Details → Save Record → Update Inventory

---

## Quick Start

### For Users
1. **Create a Purchase:** Go to `/round-wood/purchases/create/`
2. **Fill the Form:** Supplier, Wood Type, Quantity, Dimensions, Cost
3. **Save:** Volume and total cost calculated automatically
4. **Complete:** Click "Mark as Completed" to add to inventory
5. **Done!** Inventory auto-updated

### For Developers
```python
# Create via API
POST /api/round-wood-purchases/
{
  "supplier": 1,
  "wood_type": 2,
  "quantity_logs": 50,
  "diameter_inches": 12.5,
  "length_feet": 16,
  "unit_cost_per_cubic_foot": 25.00
}

# Complete (auto-updates inventory)
POST /api/round-wood-purchases/1/complete/
```

---

## Key Features

✅ **Simple Recording** - One form, minimal fields  
✅ **Auto Calculations** - Volume and cost computed automatically  
✅ **Auto Inventory** - Completing a purchase updates inventory instantly  
✅ **Fast Entry** - No approval workflow, no multiple steps  
✅ **Filtering** - Search by supplier, wood type, status, date  
✅ **History** - View all past purchases  
✅ **REST API** - Full API for programmatic access  
✅ **Admin Panel** - Django admin for management  

---

## What Changed?

### OLD System (Removed)
- ❌ Complex approval workflow (Draft → Ordered → Delivered → Paid)
- ❌ Separate line items table
- ❌ Multiple status fields
- ❌ Inspection workflow
- ❌ Audit logs
- ❌ 6+ steps per purchase

### NEW System (Implemented)
- ✅ Simple workflow (Pending → Completed or Cancelled)
- ✅ Single record per purchase
- ✅ Streamlined status
- ✅ Direct purchasing
- ✅ Auto inventory update
- ✅ 2 steps per purchase

---

## Documentation

### Choose Your Read

**[For Everyone]** Quick Overview  
→ Start with this README

**[For Users]** 📖 ROUND_WOOD_QUICK_START.md  
→ How to use the system, common tasks, examples

**[For Developers]** 📘 ROUND_WOOD_SIMPLIFIED_SYSTEM.md  
→ Complete technical documentation, models, API, database

**[For Admins]** 📋 ROUND_WOOD_IMPLEMENTATION_STATUS.md  
→ What was changed, status of each component, deployment info

**[For Implementation]** 📊 ROUND_WOOD_IMPLEMENTATION_CHANGES.md  
→ What was removed/added, URLs, breaking changes, migration

---

## Architecture

### Models

**RoundWoodPurchase** - Single record for one purchase
- Supplier & Wood Type
- Dimensions (quantity, diameter, length)
- Auto-calculated volume and total cost
- Status: pending, completed, or cancelled
- Auto-updates inventory when completed

**RoundWoodInventory** - Current stock levels (auto-managed)
- Total logs in stock
- Total volume in cubic feet
- Total cost invested
- Average cost per cubic foot
- Updated automatically when purchases are completed

**WoodType** - Reference table
- Wood species and properties
- Optional default dimensions

### Process Flow

```
┌─────────────────────────────────────────┐
│  1. Create Purchase Record              │
│     - Select Supplier                   │
│     - Select Wood Type                  │
│     - Enter Quantity & Dimensions       │
│     - Enter Cost                        │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  2. Save Purchase                       │
│     - Volume auto-calculated            │
│     - Total cost auto-calculated        │
│     - Status: "pending"                 │
└─────────────────────────────────────────┘
         ↓
    Choose One:
         ↙           ↘
┌───────────────┐  ┌──────────────┐
│ 3a. Complete  │  │ 3b. Cancel   │
│ - Mark Done   │  │ - Void       │
│ - Auto Update │  │ (skip inv)   │
│   Inventory   │  │              │
└───────────────┘  └──────────────┘
```

---

## Navigation

### Web Interface
- **Dashboard:** `/round-wood/` - Summary and recent purchases
- **Purchases:** `/round-wood/purchases/` - List all purchases
- **New Purchase:** `/round-wood/purchases/create/` - Record new purchase
- **Purchase Detail:** `/round-wood/purchases/{id}/` - View/manage purchase
- **Inventory:** `/round-wood/inventory/` - Current stock levels
- **Wood Types:** `/round-wood/wood-types/` - Reference list

### REST API
- **Base:** `/api/round-wood-purchases/`
- **List:** `GET /api/round-wood-purchases/`
- **Create:** `POST /api/round-wood-purchases/`
- **Detail:** `GET /api/round-wood-purchases/{id}/`
- **Complete:** `POST /api/round-wood-purchases/{id}/complete/`
- **Cancel:** `POST /api/round-wood-purchases/{id}/cancel/`
- **Summary:** `GET /api/round-wood-purchases/summary/`
- **Pending:** `GET /api/round-wood-purchases/pending/`

### Admin Interface
- **URL:** `/admin/`
- **Models:** RoundWoodPurchase, RoundWoodInventory, WoodType
- **Permissions:** Admin access required

---

## Common Tasks

### Record a Purchase
1. `/round-wood/purchases/create/`
2. Fill form
3. Click "Save Purchase"
4. View created purchase
5. Click "Mark as Completed"
6. ✅ Inventory updated automatically

### View All Purchases
1. `/round-wood/purchases/`
2. See list with filters
3. Use filters: Status, Supplier, Wood Type
4. Click purchase to view details

### Check Inventory
1. `/round-wood/inventory/`
2. See current stock by wood type
3. See total volume and cost invested
4. See average cost per cubic foot

### Cancel a Purchase
1. Navigate to purchase detail
2. If status is "pending":
   - Click "Cancel Purchase"
3. Purchase marked as cancelled
4. Inventory NOT updated

---

## Data Fields

### Purchase Record

| Field | Type | Notes |
|-------|------|-------|
| Supplier | ForeignKey | Who sold the logs |
| Wood Type | ForeignKey | Type of wood |
| Quantity | Integer | Number of logs |
| Diameter | Decimal | Log width in inches |
| Length | Decimal | Log length in feet |
| Volume | Decimal | **AUTO-CALCULATED** from dimensions |
| Unit Cost | Decimal | Cost per cubic foot (₱) |
| Total Cost | Decimal | **AUTO-CALCULATED** volume × unit_cost |
| Status | Choice | pending, completed, cancelled |
| Date | Date | When purchase was made |
| Notes | Text | Optional notes |
| Created By | User | Who recorded it |
| Created At | DateTime | Timestamp |
| Updated At | DateTime | Timestamp |

### Inventory Record

| Field | Type | Notes |
|-------|------|-------|
| Wood Type | OneToOne | Link to wood type |
| Logs in Stock | Integer | Count of logs |
| Volume | Decimal | Total cubic feet |
| Cost Invested | Decimal | Total ₱ spent |
| Avg Cost/cu ft | Decimal | **AUTO-CALCULATED** |
| Location | String | Warehouse location (optional) |
| Last Updated | DateTime | When inventory last changed |

---

## Status Values

**Pending** - Purchase recorded, not yet completed
- Can be: marked completed, cancelled

**Completed** - Purchase finalized and added to inventory
- Cannot be: cancelled

**Cancelled** - Purchase voided, not added to inventory
- Cannot be: changed to another status

---

## Volume Calculation

Formula:
```
Volume (cubic feet) = π × (diameter_feet/2)² × length_feet × quantity

Where:
- diameter_feet = diameter_inches ÷ 12
- All dimensions must be > 0
- Automatically calculated on save
```

Example:
```
50 logs of 12.5" diameter, 16 feet long:
- Volume per log = π × (0.521)² × 16 = 13.7 cu ft
- Total = 13.7 × 50 = 685 cu ft
```

---

## Inventory Auto-Update

When you mark a purchase as "Completed":

1. **Get or Create** RoundWoodInventory for the wood type
2. **Add Logs:** total_logs += quantity_logs
3. **Add Volume:** total_cubic_feet += volume_cubic_feet
4. **Add Cost:** total_cost_invested += total_cost
5. **Recalculate:** average_cost_per_cubic_foot = total_cost ÷ total_volume
6. **Update:** last_stock_in_date = today

**Result:** No manual inventory entry needed! ✅

---

## API Examples

### Create Purchase
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
    "purchase_date": "2024-12-15"
  }'
```

### Get Summary
```bash
curl http://localhost:8000/api/round-wood-purchases/summary/ \
  -H "Authorization: Token YOUR_TOKEN"

# Response:
{
  "total_purchases": 5,
  "total_volume_cubic_feet": 2500.50,
  "total_spent": 62512.50,
  "status_breakdown": {
    "pending": 1,
    "completed": 4,
    "cancelled": 0
  },
  "pending_purchases": 1,
  "completed_purchases": 4
}
```

### Filter by Status
```bash
curl "http://localhost:8000/api/round-wood-purchases/?status=pending" \
  -H "Authorization: Token YOUR_TOKEN"
```

### Complete a Purchase
```bash
curl -X POST http://localhost:8000/api/round-wood-purchases/1/complete/ \
  -H "Authorization: Token YOUR_TOKEN"
```

---

## Admin Panel

Access via `/admin/` (superuser required)

### RoundWoodPurchase Admin
- **List View:** See all purchases with filters
- **Detail View:** Edit purchase information
- **Bulk Actions:** Available for selected records
- **Search:** By supplier, wood type, notes
- **Filters:** By status, supplier, wood type, date

### RoundWoodInventory Admin
- **Read-only:** All stock levels auto-managed
- **View Only:** Manually editing not recommended
- **Reference:** Check current inventory

### WoodType Admin
- **Manage:** Add/edit wood types
- **Fields:** Name, species, description, defaults
- **Use:** Reference for purchases

---

## File Locations

### Key Files
```
app_round_wood/
  ├─ models.py              # RoundWoodPurchase, RoundWoodInventory
  ├─ views.py               # REST API ViewSets
  ├─ views_ui.py            # Web interface views
  ├─ serializers.py         # JSON serializers
  ├─ urls_ui.py             # Web URL patterns
  ├─ admin.py               # Django admin
  └─ migrations/
      └─ 0004_*.py          # Database migration

templates/round_wood/
  ├─ dashboard.html         # Dashboard view
  ├─ purchase_create.html   # Create form
  ├─ purchase_detail.html   # Detail view
  ├─ purchase_list.html     # List view
  ├─ inventory_list.html    # Inventory view
  └─ wood_types_list.html   # Wood type reference

Documentation/
  ├─ ROUND_WOOD_QUICK_START.md         # This file
  ├─ ROUND_WOOD_SIMPLIFIED_SYSTEM.md   # Technical docs
  └─ ROUND_WOOD_IMPLEMENTATION_*.md    # Implementation details
```

---

## Troubleshooting

**Issue:** Volume shows as 0  
**Solution:** Check diameter and length are entered and > 0

**Issue:** Inventory not updating  
**Solution:** Make sure to click "Mark as Completed" (not just save)

**Issue:** Can't find a purchase  
**Solution:** Use filters on purchase list page

**Issue:** Permission denied  
**Solution:** Make sure you're logged in as a valid user

**Issue:** URL not found  
**Solution:** Use new URL names (purchase_list, not po_list)

---

## Related Systems

**Supplier Management** → `/admin/supplier/`
- Manage suppliers for wood purchases
- Track supplier contact info
- View supplier history

**Inventory Management** → `/inventory/management/`
- Manage finished lumber inventory
- Track stock levels
- Record inventory adjustments

**Sales Orders** → `/sales/`
- Sell finished products to customers
- Track deliveries and receipts

---

## Performance Notes

- **Pagination:** 20 items per page (list views)
- **Indexes:** Optimized for supplier, status, wood type filtering
- **Calculations:** Volume computed on save (cached in DB)
- **Scaling:** Can handle thousands of purchases

---

## Security

- ✅ Authentication required for all views
- ✅ Permission checks in place
- ✅ No direct database access
- ✅ Input validation on all forms
- ✅ CSRF protection enabled
- ✅ SQL injection protected (ORM)

---

## Browser Compatibility

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

---

## Support

**Documentation Location:**
- User Guide: `ROUND_WOOD_QUICK_START.md`
- Technical Guide: `ROUND_WOOD_SIMPLIFIED_SYSTEM.md`
- Implementation: `ROUND_WOOD_IMPLEMENTATION_CHANGES.md`
- Status: `ROUND_WOOD_IMPLEMENTATION_STATUS.md`

**Need Help?**
1. Check relevant documentation
2. Review admin panel
3. Check system logs
4. Test via browsable API

---

## Version History

**v1.0 (Simplified)** - Dec 15, 2024
- Replaced complex multi-step system
- Implemented auto-calculations
- Added auto-inventory update
- Streamlined to 2 steps per purchase
- Full API and UI

---

## License & Support

Maintained as part of Lumber Management System.  
For support, refer to documentation or system administrator.

---

**Last Updated:** December 15, 2024  
**Status:** ✅ Production Ready  
**Version:** 1.0 Simplified


# Lumbering Service - Quick Start Guide

## Access the System

**Web Dashboard:** `http://localhost:8000/lumbering/`

**Admin Interface:** `http://localhost:8000/admin/` → Lumbering Service

## Basic Workflow

### Step 1: Create Service Order (2 minutes)

Go to `/lumbering/orders/create/` or click "New Service Order"

**Fill in:**
- Customer name
- Wood type (e.g., "Mahogany", "Pine")
- Number of logs
- Service fee per board foot (default: ₱5.00)
- Shavings ownership (Company, Customer, or 50/50)

Click "Create Service Order"

### Step 2: Record Lumber Output (3 minutes per batch)

View the order, click "Add Output"

**Enter for each lumber batch:**
- Lumber type (e.g., "2x4", "1x12")
- Quantity of pieces
- Length, width, thickness dimensions
- Grade (optional)

**Board feet auto-calculates:**
- Formula: (Length × Width × Thickness ÷ 12) × Quantity

Click "Save Output" → Service fee auto-updates

### Step 3: Record Shavings (1 minute)

Click "Add Shavings Record"

**Enter:**
- Quantity of shavings
- Unit (kg, tons, cubic meters, or bags)
- Notes (optional)

**Ownership auto-sets** based on order configuration

Click "Record Shavings"

### Step 4: View Summary

Refresh order detail page to see:
- Total board feet (sum of all outputs)
- Total service fee (calculated automatically)
- All shavings records with ownership

## Dashboard View

At `/lumbering/` you see:
- Quick statistics (total orders, pending, completed)
- Total service fees collected
- Recent orders with status
- Filter and action buttons

## Key Calculations

### Board Feet Formula
```
BF = (Length in feet × Width in inches × Thickness in inches ÷ 12) × Quantity
```

**Quick examples:**
- 10 pcs of 2×4, 12 feet long = 80 BF
- 5 pcs of 1×12, 10 feet long = 50 BF
- 20 pcs of 4×4, 8 feet long = 213.33 BF

### Service Fee Formula
```
Total Fee = Total Output BF × Fee Per BF
```

**Quick examples:**
- 500 BF × ₱5.00/BF = ₱2,500.00
- 1,000 BF × ₱8.00/BF = ₱8,000.00

## Shavings Ownership Quick Reference

| Setting | Customer | Company |
|---------|----------|---------|
| Customer | 100% | 0% |
| Lumber Company | 0% | 100% |
| Shared (50/50) | 50% | 50% |

Once set in the order, all shavings records auto-follow this split.

## API Quick Reference

**Create Order:**
```bash
curl -X POST http://localhost:8000/api/lumbering-service-orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer": 1,
    "wood_type": "Mahogany",
    "quantity_logs": 5,
    "service_fee_per_bf": "5.00",
    "shavings_ownership": "lumber_company"
  }'
```

**Add Output:**
```bash
curl -X POST http://localhost:8000/api/lumbering-service-outputs/ \
  -H "Content-Type: application/json" \
  -d '{
    "service_order": 1,
    "lumber_type": "2x4",
    "quantity_pieces": 50,
    "length_feet": "12.00",
    "width_inches": "3.50",
    "thickness_inches": "1.50"
  }'
```

**Record Shavings:**
```bash
curl -X POST http://localhost:8000/api/shavings-records/ \
  -H "Content-Type: application/json" \
  -d '{
    "service_order": 1,
    "quantity": "850",
    "unit": "kg"
  }'
```

**Get Order Summary:**
```bash
curl http://localhost:8000/api/lumbering-service-orders/1/summary/
```

## Status Values

- **Pending** (default) - Order created, waiting to start
- **In Progress** - Currently being milled
- **Completed** - All outputs recorded, fees finalized
- **Cancelled** - Order cancelled

## Features Highlights

✅ **Automatic calculations** - Board feet and fees computed instantly  
✅ **No approvals needed** - Direct workflow, minimal steps  
✅ **Flexible ownership** - Shavings can be split any way  
✅ **Customer tracking** - Integrated with customer database  
✅ **Simple web UI** - Easy forms for data entry  
✅ **Full API** - Integrate with other systems  
✅ **Admin dashboard** - Complete management interface  

## Typical Timeline

| Activity | Time | Notes |
|----------|------|-------|
| Create order | 2 min | One-time setup |
| Record each lumber batch | 3 min | ~10 batches typical |
| Record shavings | 1 min | Usually once per order |
| View summary | <1 min | Auto-calculated |
| **Total per order** | **30-40 min** | **For typical 10-batch milling** |

## Tips & Best Practices

1. **Set correct fees upfront** - Change default ₱5.00 if needed
2. **Choose shavings ownership once** - Set it when creating order
3. **Record outputs as you mill** - Don't wait until end
4. **Use descriptive lumber types** - "2x4 rough" vs "2x4 planed"
5. **Add quality grades** - Helps with pricing and quality tracking
6. **Notes field** - Document any special requirements or issues

## Support

For issues or questions, check:
- Full documentation: `LUMBERING_SERVICE_IMPLEMENTATION.md`
- Django Admin: `http://localhost:8000/admin/`
- API docs: `http://localhost:8000/api/` (auto-generated)

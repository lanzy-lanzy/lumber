# Quick Start: Auto-Generated PO Numbers & COD

## What's New?

### ✓ PO Numbers Auto-Generated
No more typing `RWPO-2024-001`. System creates it automatically!

### ✓ Default COD Payment Terms
Field pre-filled with "Cash on Delivery (COD)" - change if needed.

---

## Creating a Purchase Order (New Process)

### Step 1: Go to Round Wood Module
```
http://localhost:8000/round-wood/
↓
Click "New Purchase Order"
```

### Step 2: Fill the Form (Notice: No PO Number Field!)

**Basic Information:**
- **PO Number**: [Auto-generated - see below after creation]
- **Supplier**: Select from dropdown ↓

**Delivery & Pricing:**
- **Expected Delivery Date**: Pick a date
- **Unit Cost**: Enter ₱ amount

**Payment Terms:**
- **Payment Terms**: Pre-filled with "Cash on Delivery (COD)"
  - Keep it as-is (default)
  - OR change to: "Net 30", "50% Advance", etc.

**Additional Notes:**
- **Notes**: Optional instructions

### Step 3: Click "Create Purchase Order"

**What happens:**
```
System automatically generates PO number like:
RWPO-2025-0001
RWPO-2025-0002
RWPO-2025-0003 (etc.)
```

### Step 4: Success Message
```
✓ Purchase order RWPO-2025-0001 created successfully
```

You can now:
- View the order
- Add items
- Submit for approval
- Continue managing

---

## Example

### Old Way (Before)
```
[PO Number Field]     RWPO-2024-001  ← Type this manually
[Supplier]            [Select dropdown]
[Delivery Date]       2024-12-25
[Unit Cost]           ₱50.00
[Payment Terms]       Cash on Delivery (COD)  ← Type this
[Notes]               Standard delivery

Result: Takes more time, manual entry needed
```

### New Way (After)
```
Auto-Generated Info: PO number will be created automatically
[Supplier]            [Select dropdown]
[Delivery Date]       2024-12-25
[Unit Cost]           ₱50.00
[Payment Terms]       Cash on Delivery (COD)  ← Pre-filled
[Notes]               Standard delivery

Result: Faster, less typing, fewer errors
```

---

## PO Number Format

### Pattern
```
RWPO-YYYY-NNNN
├── RWPO = Round Wood PO (prefix)
├── YYYY = Year (2025, 2026, etc.)
└── NNNN = Sequential number (0001, 0002, etc.)
```

### Examples
```
RWPO-2025-0001  First order in 2025
RWPO-2025-0002  Second order in 2025
RWPO-2025-0003  Third order in 2025
RWPO-2026-0001  First order in 2026 (year change resets)
```

---

## Payment Terms Options

### Default (Pre-filled)
```
Cash on Delivery (COD)
```

### Common Alternatives
```
Net 30          Payment due in 30 days
Net 60          Payment due in 60 days
2/10 Net 30     2% discount if paid in 10 days
50% Advance     Half before, half after delivery
Advance Payment Full payment before delivery
```

---

## FAQ Quick Answers

**Q: Where's the PO Number field?**
A: Removed! It's auto-generated. You'll see it after creation.

**Q: Can I change the PO number?**
A: No, once created it's fixed. Design your custom format before go-live.

**Q: Can I have my own PO format?**
A: Currently it's RWPO-YYYY-NNNN. Contact support for custom formats.

**Q: What if I need different payment terms?**
A: Just edit the field. Default is COD but you can change each order.

**Q: What if I forget payment terms?**
A: Don't worry - it auto-fills with COD. You only need to change if different.

**Q: Can numbers duplicate?**
A: No, database prevents duplicates. Unique across all time.

---

## Benefits Summary

| Before | After |
|--------|-------|
| ❌ Manual PO number entry | ✅ Auto-generated |
| ❌ Risk of duplicates | ✅ Guaranteed unique |
| ❌ Inconsistent formats | ✅ Standard format |
| ❌ Type COD every time | ✅ Pre-filled |
| ❌ Slower form filling | ✅ Faster creation |

---

## Keyboard Shortcuts

**While filling form:**
- `Tab` → Move to next field
- `Shift+Tab` → Move to previous field
- `Enter` → Submit form (from last field)
- `Esc` → Cancel and go back

---

## Common Issues & Solutions

### Issue: Can't find PO Number field
**Solution**: It's gone! It's auto-generated. Look for the info box that says "PO number will be auto-generated"

### Issue: Payment Terms is empty
**Solution**: It shouldn't be. If empty, refresh the page. It defaults to "Cash on Delivery (COD)"

### Issue: Created but can't find PO
**Solution**: Check the success message - it shows the generated PO number. Click "View Order" link.

---

## Next Steps After Creation

1. **View Order**: See details and confirmation
2. **Add Items**: Add wood types and quantities
3. **Submit**: Send for approval
4. **Track**: Monitor delivery and inspection
5. **Complete**: Stock inventory

---

## Dashboard Workflow

```
Dashboard
  ↓
[New Purchase Order] → Create Form
  ↓
Auto-Generate PO Number
  ↓
Order Created ✓
  ↓
View Order Detail
  ↓
Add Items / Submit / etc.
```

---

## Support

If you need help:
1. Check the form help text (hover over ℹ️ icons)
2. See AUTO_PO_AND_COD_FEATURE.md for detailed docs
3. Review AUTO_PO_COD_SUMMARY.md for technical info
4. Contact admin for custom configurations

---

**Quick Start Version**: 1.0
**Last Updated**: 2025
**Module**: Round Wood Purchasing

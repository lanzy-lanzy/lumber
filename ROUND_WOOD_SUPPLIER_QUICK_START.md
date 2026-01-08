# Round Wood Supplier Creation - Quick Start

## What's New?
A green "+" button next to the Supplier dropdown on the Round Wood Purchase page that lets you create new suppliers without leaving the form.

## How to Use

### Step 1: Open Round Wood Purchase Form
- Go to: **Round Wood** → **Purchases** → **Record New Purchase**
- URL: `http://localhost:8000/round-wood/purchases/create/`

### Step 2: Create New Supplier
1. Click the green **"+" button** next to the Supplier dropdown
2. A modal dialog will appear
3. Fill in required fields:
   - **Company Name** (required)
   - **Contact Person** (required)
   - **Phone Number** (required)
   - **Email** (optional)
   - **Address** (optional)
4. Click **"Create Supplier"** button

### Step 3: Complete Purchase
1. New supplier is auto-selected in dropdown
2. Continue filling the form:
   - Wood Type
   - Number of Logs
   - Diameter (inches)
   - Length (feet)
   - Unit Cost per Cubic Foot
   - Purchase Date
   - Notes
3. Click **"Save Purchase"**

## Required Information
| Field | Required | Notes |
|-------|----------|-------|
| Company Name | Yes | Full company name |
| Contact Person | Yes | Who to contact |
| Phone Number | Yes | Contact phone |
| Email | No | Optional |
| Address | No | Optional but helpful |

## Features
✓ Fast - No page reload
✓ Easy - Only 3 required fields
✓ Smart - Auto-selects new supplier
✓ Smooth - Non-intrusive modal
✓ Responsive - Works on all devices

## Modal Controls
| Action | Method |
|--------|--------|
| Open | Click green "+" button |
| Close | Click "X" button |
| Close | Click "Cancel" button |
| Close | Click outside modal |
| Submit | Click "Create Supplier" |

## Error Messages
| Error | Solution |
|-------|----------|
| "Company name is required" | Enter the company name |
| "Contact person is required" | Enter contact person's name |
| "Phone number is required" | Enter a phone number |
| "Error creating supplier" | Check connection or try again |

## Tips
- Company Name field is auto-focused for quick entry
- Email and Address fields are optional
- New supplier can be used immediately
- Supplier will be available for future purchases

## What Gets Saved
When you create a supplier:
- Company name
- Contact person's name
- Phone number
- Email (if provided)
- Address (if provided)
- Creation timestamp
- Active status (auto-set to active)

The supplier is then available in:
- This purchase form
- All future purchase forms
- Supplier management
- Purchase orders
- All other supplier-related features

## Keyboard Shortcuts
- **Tab** - Move between fields
- **Enter** - Submit form (when in field)
- **Esc** - Close modal (when outside form)

## Troubleshooting

**Modal won't open?**
- Try clicking the green "+" button again
- Check browser console (F12)
- Try refreshing the page

**Supplier not saving?**
- Ensure all 3 required fields are filled
- Check that you have internet connection
- Look for red error messages

**New supplier not in dropdown?**
- Check if creation was successful (green toast message)
- Try refreshing the page
- Try again with different information

**Getting validation error?**
- Fill in all required fields (marked with red *)
- Use valid phone number format
- Use valid email format (if entering email)

## Browser Support
Works in:
- Chrome/Edge
- Firefox
- Safari
- Mobile browsers

## Similar Features
This same feature is available for:
- **Lumbering Service**: Create walk-in customers
- Check: `WALKIN_CUSTOMER_LUMBERING.md`

## Questions?
Refer to full documentation: `ROUND_WOOD_WALKIN_SUPPLIER.md`

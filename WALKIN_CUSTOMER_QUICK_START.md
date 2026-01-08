# Walk-in Customer Feature - Quick Start Guide

## What Was Added?
A green "+" button on the lumbering service order creation page that allows you to create new walk-in customers without leaving the form.

## How to Use

### Step 1: Open Order Creation
- Go to **Lumbering Service** → **Orders** → **Create New Service Order**
- URL: `http://localhost:8000/lumbering/orders/create/`

### Step 2: Create Walk-in Customer
1. Click the green **"+" button** next to the Customer dropdown
2. A modal dialog will appear
3. Fill in the required fields:
   - **Full Name** (required) - Customer's name
   - **Phone Number** (required) - Contact number
   - **Email** (optional)
   - **Address** (optional)
4. Click **"Create Customer"** button

### Step 3: Continue with Order
1. The new customer will automatically appear in the dropdown and be selected
2. Continue filling the rest of the form:
   - Received Date
   - Wood Type
   - Number of Logs
   - Service Fee per Board Foot
   - Shavings Ownership
   - Notes
3. Click **"Create Service Order"** to save

## Features
✓ Fast customer registration without page reload
✓ Modal dialog for quick entry
✓ Auto-selection of newly created customer
✓ Real-time validation
✓ Success/error notifications
✓ Mobile-friendly design
✓ Keyboard accessible

## What Gets Saved?
When you create a walk-in customer:
- Customer name
- Phone number
- Email (if provided)
- Address (if provided)
- Creation timestamp
- Added to existing customer list

The customer can then be used for:
- Future lumbering service orders
- Sales orders
- All other customer-related features

## Error Messages
| Error | Solution |
|-------|----------|
| "Customer name is required" | Enter the customer's full name |
| "Phone number is required" | Enter a valid phone number |
| "Please select or create a customer" | Create a new customer or select from dropdown |
| "Error creating customer" | Try again or check connection |

## Keyboard Shortcuts
- **Tab**: Move between fields
- **Enter**: Submit form (when in field) or click button
- **Esc**: Close modal (when outside form)

## Troubleshooting

**Modal won't close?**
- Click the X button in the top-right
- Click "Cancel" button
- Click outside the modal

**New customer not appearing?**
- Check if the form was submitted successfully (green toast)
- Refresh the page
- Try again

**Getting validation errors?**
- Ensure name and phone are filled
- Remove any special characters
- Use valid email format if entering email

## Integration
Walk-in customers created here are fully integrated into the system and can be:
- Selected for future orders
- Used in sales transactions
- Viewed in customer management
- Updated with additional information later

## Questions?
Refer to the full documentation: `WALKIN_CUSTOMER_LUMBERING.md`

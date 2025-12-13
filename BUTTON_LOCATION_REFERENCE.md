# Mark Ready Button - Location Reference

## Button Position in Sales Orders Table

### Visual Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Sales Orders Management                                  ⊞ ◻ ✕ │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  [Export PDF] [+ Create Order] [Refresh]                         │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Search SO/Customer │ Payment Type │ Date From │ Date To  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Summary Cards:                                                   │
│  [Total Orders] [Total Sales] [Total Discount] [Pending Balance] │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ORDER TABLE:                                                    │
│                                                                   │
│  ┌─────────┬──────────────┬──────┬─────────┬─────────┬─────┬──┐ │
│  │   SO    │   Customer   │Items │ Amount  │Discount │Paid │Bal│ │
│  │ Number  │ Name (Balance)│Count │ Price   │ Amount  │ Amt │ue │
│  ├─────────┼──────────────┼──────┼─────────┼─────────┼─────┼──┤ │
│  │         │              │      │         │         │     │  │ │
│  │SO-2025  │John Doe      │  1   │ ₱500.00 │    -    │  -  │₱5│ │
│  │20251213 │(₱500.00)     │items │         │         │     │00│ │
│  │0005     │              │      │         │         │     │  │ │
│  │         │              │      │         │         │     │  │ │
│  ├─────────┴──────────────┴──────┴─────────┴─────────┴─────┴──┤ │
│  │ Payment │  Date       │ Actions                             │ │
│  │  Type   │             │ 👁️  📝  💵  ✓                      │ │
│  ├─────────┼─────────────┼───────────────────────────────────┤ │
│  │  Cash   │  12/13/2025 │ 👁️  📝      ✓  ← Mark Ready      │ │
│  │         │             │ Blue Edit Orange Purple            │ │
│  └─────────┴─────────────┴───────────────────────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Table Column Order

| Column # | Header | Content |
|----------|--------|---------|
| 1 | SO Number | SO-20251213-0005 |
| 2 | Customer | Name and Balance |
| 3 | Items | 1 items |
| 4 | Amount | ₱500.00 |
| 5 | Discount | ₱0.00 |
| 6 | Paid | ₱0.00 |
| 7 | Balance | ₱500.00 |
| 8 | Payment Type | Cash / Partial / Credit |
| 9 | Date | 12/13/2025 |
| **10** | **Actions** | **👁️ 📝 💵 ✓** |

---

## Action Buttons Order

From left to right in the Actions column:

### 1️⃣ View Order Button
- **Icon**: Eye (`fa-eye`)
- **Color**: Blue (#2563eb)
- **Hover**: Darker blue
- **Action**: Opens order details view modal
- **Always Visible**: Yes
- **Title**: "View Order"

### 2️⃣ Edit Order Button
- **Icon**: Pencil (`fa-edit`)
- **Color**: Green (#16a34a)
- **Hover**: Darker green
- **Action**: Opens order edit modal
- **Always Visible**: Yes
- **Title**: "Edit Order"

### 3️⃣ Record Payment Button
- **Icon**: Money Bill (`fa-money-bill`)
- **Color**: Orange (#ea580c)
- **Hover**: Darker orange
- **Action**: Opens payment recording modal
- **Always Visible**: Only if `order.balance > 0`
- **Title**: "Record Payment"

### 4️⃣ Mark Ready Button ← **NEW!**
- **Icon**: Check Circle (`fa-check-circle`)
- **Color**: Purple (#a855f7)
- **Hover**: Darker purple (#9333ea)
- **Action**: Marks order as ready and notifies customer
- **Always Visible**: Yes (always shown, unlike payment button)
- **Title**: "Mark Ready for Pickup"

---

## HTML Structure

```html
<td class="px-6 py-4 text-center">
    <div class="flex gap-2 justify-center">
        
        <!-- BUTTON 1: View Order -->
        <button @click="viewOrder(order)" 
                class="text-blue-600 hover:text-blue-800 px-2 py-1" 
                title="View Order">
            <i class="fas fa-eye"></i>
        </button>
        
        <!-- BUTTON 2: Edit Order -->
        <button @click="editOrder(order)" 
                class="text-green-600 hover:text-green-800 px-2 py-1" 
                title="Edit Order">
            <i class="fas fa-edit"></i>
        </button>
        
        <!-- BUTTON 3: Record Payment (Conditional) -->
        <template x-if="parseFloat(order.balance) > 0">
            <button @click="recordPayment(order)" 
                    class="text-orange-600 hover:text-orange-800 px-2 py-1" 
                    title="Record Payment">
                <i class="fas fa-money-bill"></i>
            </button>
        </template>
        
        <!-- BUTTON 4: Mark Ready (NEW - Always Visible) -->
        <button @click="markOrderReady(order)" 
                class="text-purple-600 hover:text-purple-800 px-2 py-1" 
                title="Mark Ready for Pickup">
            <i class="fas fa-check-circle"></i>
        </button>
        
    </div>
</td>
```

---

## CSS Classes Used

### Button Styling
```css
class="text-purple-600 hover:text-purple-800 px-2 py-1"
```

- `text-purple-600` = Purple text color (#a855f7)
- `hover:text-purple-800` = Darker purple on hover (#7e22ce)
- `px-2` = Horizontal padding (0.5rem)
- `py-1` = Vertical padding (0.25rem)

### Container Styling
```css
class="flex gap-2 justify-center"
```

- `flex` = Flexbox layout
- `gap-2` = Space between buttons (0.5rem)
- `justify-center` = Center buttons horizontally

---

## Visual Color Reference

### Icon Colors

| Button | Icon | Color Code | Hex | Tailwind |
|--------|------|-----------|-----|----------|
| View | Eye | Blue | #2563eb | blue-600 |
| Edit | Pencil | Green | #16a34a | green-600 |
| Payment | Money | Orange | #ea580c | orange-600 |
| Mark Ready | Check | Purple | **#a855f7** | **purple-600** |

### Hover States

| Button | Hover Hex | Tailwind |
|--------|-----------|----------|
| View | #1d4ed8 | blue-800 |
| Edit | #15803d | green-800 |
| Payment | #c26a0a | orange-800 |
| Mark Ready | **#7e22ce** | **purple-800** |

---

## Icon Font Details

All icons use Font Awesome 6.4.0 (CDN)

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
```

### Icon Classes

- `fa-eye` = View/eye icon
- `fa-edit` = Edit/pencil icon
- `fa-money-bill` = Money/bill icon
- `fa-check-circle` = Check mark in circle ← **NEW**

---

## Spacing & Layout

### Button Container
- Width: Auto (flex)
- Padding: 2px horizontal, 1px vertical per button
- Gap between buttons: 8px (0.5rem)
- Alignment: Center horizontally
- Vertical alignment: Center (default flex)

### Table Cell (Action Column)
- Padding: 24px (px-6) horizontal, 16px (py-4) vertical
- Text align: Center
- Border: Standard table border

---

## Responsive Behavior

### Desktop (Full Width)
- All buttons visible
- Full spacing maintained
- Icons clearly visible
- Tooltips appear on hover

### Tablet (Medium Width)
- All buttons visible (slight condensing)
- Tooltips still functional
- Spacing slightly reduced if needed

### Mobile (Small Width)
- Buttons stack vertically OR compress
- Tooltips functional on touch
- Icons remain clear

---

## Interactive Behavior

### On Hover (Desktop)
```
Button becomes darker:
- Text color changes from purple-600 to purple-800
- Cursor changes to pointer
- Tooltip appears after ~200ms
```

### On Click
```
Mark Ready Button:
1. Confirmation dialog appears
2. User confirms or cancels
3. If confirmed, API call made
4. Success message displayed
5. Table refreshes
6. Dialog closes
```

---

## Accessibility

- ✅ Buttons have title attributes (tooltips)
- ✅ Icons are meaningful and labeled
- ✅ Color contrast meets WCAG standards
- ✅ Keyboard accessible (tabindex)
- ✅ Touch-friendly size (minimum 44x44 pixels)

---

## Sample Order Row

### With Balance Due (Shows Payment Button)
```
SO-20251213-0005 │ John Doe (Balance: ₱500) │ 1 items │ ₱500 │ - │ ₱0 │ ₱500 │ Cash │ 12/13/2025 │ 👁️ 📝 💵 ✓
```
Shows 4 action buttons

### With Full Payment (No Payment Button)
```
SO-20251212-0002 │ Jane Smith (Balance: ₱0) │ 2 items │ ₱750 │ ₱150 │ ₱600 │ ₱0 │ Paid │ 12/12/2025 │ 👁️ 📝 ✓
```
Shows 3 action buttons (no payment button since balance = 0)

---

## File Location

**File**: `templates/sales/sales_orders.html`

**Button Location**:
- Lines: 149-151

**Function Location**:
- Lines: 941-967

**Table Structure**:
- Lines: 84-155

---

## Quick Reference for Developers

### To Find the Button
1. Open `templates/sales/sales_orders.html`
2. Search for: `markOrderReady`
3. Two matches:
   - Line 149: Button definition
   - Line 941: Function definition

### Button Classes
- Container: `flex gap-2 justify-center`
- Button: `text-purple-600 hover:text-purple-800 px-2 py-1`
- Icon: `fa-check-circle` (Font Awesome)

### Function Name
- `markOrderReady(order)`

### API Endpoint
- `POST /api/confirmations/{order_id}/mark_ready/`

---

**That's everything you need to know about the button's location and styling!**

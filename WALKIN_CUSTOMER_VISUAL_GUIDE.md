# Walk-in Customer Feature - Visual Guide

## UI Layout

### Main Form - Customer Section
```
┌─────────────────────────────────────────────────────────┐
│  👤 Customer Information                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ⭐ Customer                  ⭐ Received Date         │
│  ┌────────────────────────┐   ┌─────────────────┐     │
│  │ -- Select a customer - │ + │   12/18/2025    │     │
│  │ Juan Dela Cruz         │ [+] │ 📅              │     │
│  │ Maria Santos           │    └─────────────────┘     │
│  │ Pedro Garcia           │                            │
│  └────────────────────────┘                            │
│  (Add more options)                                    │
│
│  [+] = Green button to create walk-in customer
└─────────────────────────────────────────────────────────┘
```

### Modal Dialog - Create Walk-in Customer
```
┌────────────────────────────────────────────────────┐
│ Create Walk-in Customer                          ✕ │
├────────────────────────────────────────────────────┤
│                                                  │
│ ⭐ Full Name                                    │
│ ┌──────────────────────────────────────────────┐ │
│ │ Customer name                                │ │
│ └──────────────────────────────────────────────┘ │
│                                                  │
│ ⭐ Phone Number                                 │
│ ┌──────────────────────────────────────────────┐ │
│ │ 09xxxxxxxxx                                  │ │
│ └──────────────────────────────────────────────┘ │
│                                                  │
│ Email (Optional)                                │
│ ┌──────────────────────────────────────────────┐ │
│ │ customer@example.com                         │ │
│ └──────────────────────────────────────────────┘ │
│                                                  │
│ Address (Optional)                              │
│ ┌──────────────────────────────────────────────┐ │
│ │ Street address...                            │ │
│ │                                              │ │
│ └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌─────────────────┐   ┌──────────────┐       │
│  │ 💾 Create       │   │ ✕ Cancel     │       │
│  │ Customer        │   │              │       │
│  └─────────────────┘   └──────────────┘       │
│                                                  │
└────────────────────────────────────────────────┘

Color Scheme:
- Green background for create action
- Gray background for cancel action
- Red star (⭐) for required fields
```

### Toast Notifications

**Success Notification:**
```
┌────────────────────────────────────────────────────┐
│ ✓ Walk-in customer created successfully!         │
└────────────────────────────────────────────────────┘
(Green background, auto-dismisses in 3 seconds)
```

**Error Notification:**
```
┌────────────────────────────────────────────────────┐
│ ✕ Please select or create a customer              │
└────────────────────────────────────────────────────┘
(Red background, auto-dismisses in 3 seconds)
```

## User Interaction Flow

### Step 1: Initial State
```
Order Creation Form
├─ Customer: [-- Select a customer --] [+]
├─ Wood Type: [______]
├─ Logs: [__]
└─ ... other fields
```

### Step 2: Click Green Button
```
Green button clicked
    ↓
Modal appears (semi-transparent overlay)
Modal receives focus
Name field auto-focused
```

### Step 3: Fill Customer Details
```
Modal Form
├─ Name: [Juan Dela Cruz        ]  ← Cursor here
├─ Phone: [09123456789           ]
├─ Email: [juan@example.com      ]
├─ Address: [123 Main Street     ]
└─ [Create Customer] [Cancel]
```

### Step 4: Submit Customer
```
Click "Create Customer"
    ↓
Validate form (client-side)
    ↓
POST request to API
    ↓
Wait for response...
    ↓
```

### Step 5: Success
```
API returns: {id: 42, name: "Juan Dela Cruz", phone: "09123456789"}
    ↓
Add to dropdown options
    ↓
Auto-select new customer
    ↓
Close modal
    ↓
Show green success toast
    ↓
Dropdown now shows:
├─ Juan Dela Cruz ✓ (selected)
└─ ... other customers
```

### Step 6: Continue Order
```
Order Creation Form
├─ Customer: [Juan Dela Cruz] ✓ (selected)
├─ Wood Type: [_____]         ← User continues here
├─ Logs: [__]
└─ ... fill remaining fields
```

## Color Reference

| Element | Color | Hex | Usage |
|---------|-------|-----|-------|
| Primary Action | Amber | #b45309 | Submit order button |
| Walk-in Button | Green | #16a34a | Create customer button |
| Cancel Button | Gray | #d1d5db | Cancel/close actions |
| Error Background | Red | #ef4444 | Error messages |
| Success Toast | Green | #22c55e | Success messages |
| Required Star | Red | #ef4444 | Required field indicator |
| Focus Ring | Amber | #fbbf24 | Field focus state |

## Button States

### Walk-in Button
```
Normal State:    [+] (Green background)
Hover State:     [+] (Darker green background)
Active State:    [+] (Pressed appearance)
```

### Submit/Create Buttons
```
Normal State:    [Text] (Full opacity)
Hover State:     [Text] (Darker shade)
Disabled State:  [Text] (Grayed out - optional future)
```

## Icon Reference

| Icon | Location | Meaning |
|------|----------|---------|
| ✕ (X) | Modal header | Close modal |
| + (Plus) | Green button | Create new customer |
| 👤 | Section header | User/customer info |
| ⭐ (Star) | Field labels | Required field |
| 💾 | Submit button | Save/create action |
| ℹ️ (Info) | Help text | Additional information |

## Responsive Design

### Desktop (1024px+)
```
┌────────────────────────────────────────────────────┐
│ Customer    [--------+]    Received Date [-----]   │
└────────────────────────────────────────────────────┘

Modal centered on screen (400px width)
```

### Tablet (768px - 1023px)
```
┌─────────────────────────────────┐
│ Customer  [-------+]             │
│ Received Date [------]           │
└─────────────────────────────────┘

Modal takes 80% of screen width
```

### Mobile (< 768px)
```
┌──────────────────────────┐
│ Customer                 │
│ [-------+]               │
│ Received Date            │
│ [----------]             │
└──────────────────────────┘

Modal full width with margins
```

## Form Validation Visual Feedback

### Valid Input
```
┌──────────────────────────┐
│ Juan Dela Cruz           │  ✓ Green border on focus
└──────────────────────────┘
```

### Invalid Input
```
┌──────────────────────────┐
│                          │  ✕ Empty required field
└──────────────────────────┘
↓
Error toast appears below
```

### Focus State
```
┌══════════════════════════┐
│ [Cursor here]            │  Green ring on focus
└══════════════════════════┘
    ↑
  Thick green border/outline
```

## Keyboard Navigation

```
Tab Key:        Move to next field
Shift + Tab:    Move to previous field
Enter:          Submit form (in modal)
Escape:         Close modal (outside form)
```

## Loading States (Future Enhancement)

```
Creating customer...
┌────────────────────────┐
│ ⏳ Creating...       │
│                    │
│  [Cancel] [OK]     │
└────────────────────┘
```

## Error States

```
Name field:     "Name is required" (inline message)
Phone field:    "Phone is required" (inline message)
API Error:      Toast: "Error creating customer" (top-right)
Network Error:  Toast: "Network error" (top-right)
```

## Accessibility Features

```
ARIA Labels:       All form fields have proper labels
Focus Management:  Auto-focus on modal open
Keyboard Support:  All controls keyboard accessible
Color Contrast:    Text meets WCAG AA standards
Screen Readers:    Semantic HTML structure
Icons + Text:      All buttons have visible text
```

## Mobile Specific

```
Touch Target Size:  44px minimum height
Modal Width:        90vw (with margins)
Keyboard:           Mobile keyboard supports input
Portrait Mode:      Form stacks vertically
Landscape Mode:     Maintains usability
```

## Animation Effects

```
Modal Entry:       Fade in (opacity 0→1)
Modal Exit:        Fade out (opacity 1→0)
Toast Appear:      Slide in from top-right
Toast Dismiss:     Fade out
Button Hover:      Color transition (200ms)
```

## Performance Indicators

```
Fast Response:      Modal opens instantly (< 50ms)
API Response:       Success notification within 300ms
Auto-dismiss:       Toast closes after 3 seconds
No Jank:            Smooth animations (60fps)
```

## Browser Compatibility Display

```
✓ Chrome      (Fully supported)
✓ Firefox     (Fully supported)
✓ Safari      (Fully supported)
✓ Edge        (Fully supported)
✕ IE 11       (Not supported - uses Fetch API)
✓ Mobile      (iOS Safari, Chrome Android)
```

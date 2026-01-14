# Dynamic Wood Type Addition Feature

## Overview
Added the ability to dynamically create new wood types directly from the Round Wood Purchase form, similar to how suppliers can be added. Users can now click a "+" button next to the Wood Type dropdown to create a new wood type without leaving the form.

## Changes Made

### 1. Template Updates (`templates/round_wood/purchase_create.html`)

#### Wood Type Field Enhancement
- Added a green "+" button next to the Wood Type dropdown (lines 52-68)
- Modified the select field to have ID `wood_type_id` for JavaScript reference
- Changed layout to `flex gap-2` to accommodate the button

#### New Modal Dialog
- Added "Create New Wood Type" modal (lines 176-220)
- Modal includes fields for:
  - **Wood Type Name** (required) - main wood type name
  - **Description** (optional) - additional notes about the wood type
- Modal design matches supplier creation modal for consistency

#### JavaScript Logic
- Added complete event handling for the wood type modal (lines 292-371)
  - Modal open/close functionality
  - Form submission via AJAX
  - Automatic dropdown update on success
  - Success/error notifications
- Maintains existing supplier modal functionality

### 2. Backend View (`app_round_wood/views_ui.py`)

Added new view function: `create_wood_type()` (lines 273-306)
- **Endpoint**: POST request handler
- **Validation**:
  - Checks that wood type name is provided
  - Prevents duplicate wood type names (case-insensitive)
- **Response**: JSON with newly created wood type ID and name
- **Error Handling**: Returns appropriate error messages

### 3. URL Configuration (`app_round_wood/urls_ui.py`)

Added new URL route:
```python
path('api/create-wood-type/', views_ui.create_wood_type, name='api_create_wood_type'),
```

## Feature Details

### User Flow
1. User opens "Record Round Wood Purchase" form
2. User clicks the green "+" button next to Wood Type dropdown
3. "Create New Wood Type" modal appears
4. User enters wood type name and optional description
5. User clicks "Create Wood Type" button
6. If successful:
   - New wood type is created in database
   - Modal closes automatically
   - New wood type appears in dropdown and is selected
   - Success notification displayed
7. If error (e.g., duplicate name):
   - Error message displayed in notification
   - Modal remains open for correction

### Validation Rules
- Wood type name is **required**
- Duplicate names are **prevented** (case-insensitive matching)
- Description is **optional**
- All new wood types are created as **active** by default

### API Response Format
**Success (201 Created)**:
```json
{
  "id": 123,
  "name": "Mahogany",
  "description": "High-quality hardwood"
}
```

**Error (400/500)**:
```json
{
  "message": "Error description"
}
```

## Design Consistency

The implementation mirrors the existing supplier creation feature:
- Same modal style and layout
- Same button appearance (green "+")
- Same notification system
- Same AJAX workflow
- Same validation approach

## Testing Recommendations

1. **Create New Wood Type**
   - Click "+" button and verify modal appears
   - Enter wood type name and submit
   - Verify new type appears in dropdown and is selected

2. **Validation**
   - Try creating with empty name (should show error)
   - Try creating duplicate name (should show error)
   - Try with only description, no name (should show error)

3. **Modal Behavior**
   - Test close button functionality
   - Test clicking outside modal
   - Test cancel button
   - Verify form resets after successful creation

4. **Integration**
   - Complete a purchase with newly created wood type
   - Verify the wood type is saved correctly
   - Check that the wood type persists in dropdown for future uses

## Database Impact

- Creates new `WoodType` entries in database
- No migrations required (uses existing `WoodType` model)
- All new types are marked as `is_active=True`

## Files Modified

1. `templates/round_wood/purchase_create.html` - Template and JavaScript
2. `app_round_wood/views_ui.py` - Backend view
3. `app_round_wood/urls_ui.py` - URL routing

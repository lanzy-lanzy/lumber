# Wood Types Population Guide

## Overview

15 wood types have been successfully populated into the database. These represent common timber species used in the lumber and construction industries.

## Wood Types Added

### Hardwoods (8)
1. **Oak Logs** - Premium hardwood for furniture and flooring
2. **Maple Logs** - Dense wood for cabinetry and flooring
3. **Birch Logs** - Fine grain for plywood and veneer
4. **Walnut Logs** - Premium wood for fine furniture
5. **Ash Logs** - Strong wood for tool handles and sports equipment
6. **Cherry Logs** - Fine-grained wood for premium furniture
7. **Elm Logs** - High impact resistance for boat building
8. **Cedar Logs** - Lightweight with natural decay resistance

### Softwoods (5)
1. **Pine Logs** - General construction and pallets
2. **Fir Logs** - Construction lumber and plywood
3. **Spruce Logs** - Construction and aircraft materials
4. **Hemlock Logs** - General construction and framing
5. **Poplar Logs** - Boxes, pallets, and veneer

### Tropical Woods (2)
1. **Mahogany Logs** - Premium tropical hardwood
2. **Teak Logs** - Exotic hardwood for outdoor use

## Properties Per Wood Type

Each wood type includes:
- **Name**: Unique identifier
- **Species Category**: hardwood, softwood, tropical, or mixed
- **Default Diameter**: Standard log diameter in inches
- **Default Length**: Standard log length in feet
- **Description**: Detailed specifications and use cases

## Population Methods

### Method 1: Django Management Command (Recommended)

```bash
python manage.py populate_wood_types
```

**Advantages:**
- Part of Django framework
- Proper error handling
- Formatted output
- Can be integrated into deployment scripts

**Output:**
```
[+] Created: 14 wood types
[*] Updated: 1 wood types
[SUCCESS] Total: 15 wood types in database
```

### Method 2: Direct Python Script

```bash
python populate_wood_types.py
```

**Advantages:**
- Standalone script
- Can be run independently
- Quick testing

### Method 3: Django Shell

```bash
python manage.py shell
```

Then:
```python
from app_round_wood.models import WoodType

WoodType.objects.create(
    name='Custom Wood',
    species='hardwood',
    default_diameter_inches=12.0,
    default_length_feet=16.0,
    description='Custom wood type'
)
```

## Accessing Wood Types

### In Django Admin
1. Go to http://localhost:8000/admin/
2. Navigate to "Round Wood Purchasing" section
3. Click on "Wood types"
4. View, create, edit, or delete wood types

### In UI
1. Go to http://localhost:8000/round-wood/
2. Click on "Wood Types" in the sidebar
3. View all available wood types with specifications

### Via API
```bash
# List all wood types
curl -H "Authorization: Bearer TOKEN" \
     http://localhost:8000/api/wood-types/

# Get specific wood type
curl -H "Authorization: Bearer TOKEN" \
     http://localhost:8000/api/wood-types/1/

# Create new wood type
curl -X POST \
     -H "Authorization: Bearer TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "New Wood Type",
       "species": "hardwood",
       "default_diameter_inches": 12.0,
       "default_length_feet": 16.0,
       "description": "Description here"
     }' \
     http://localhost:8000/api/wood-types/
```

## Using Wood Types in Purchase Orders

### Creating Purchase Order with Wood Items

1. Create a purchase order (see Round Wood module)
2. In the order, add wood items by selecting from the populated wood types
3. The system will automatically use the default dimensions
4. Override dimensions if needed for specific orders

### Example: Creating PO Item

```python
from app_round_wood.models import (
    RoundWoodPurchaseOrder,
    RoundWoodPurchaseOrderItem,
    WoodType
)

# Get a wood type
oak = WoodType.objects.get(name='Oak Logs')

# Create PO item
item = RoundWoodPurchaseOrderItem.objects.create(
    purchase_order=po,
    wood_type=oak,
    quantity_logs=100,
    diameter_inches=oak.default_diameter_inches,
    length_feet=oak.default_length_feet,
    unit_cost_per_cubic_foot=50.00
)
```

## Database Structure

### WoodType Model Fields

```python
class WoodType(models.Model):
    name                    # CharField, max_length=200, unique
    species                 # CharField with choices: hardwood, softwood, tropical, mixed
    description             # TextField, optional
    default_diameter_inches # DecimalField, optional
    default_length_feet     # DecimalField, optional
    is_active               # BooleanField, default=True
    created_at              # DateTimeField, auto_now_add
    updated_at              # DateTimeField, auto_now
```

## Management Commands

### populate_wood_types.py

**Location:** `app_round_wood/management/commands/populate_wood_types.py`

**Features:**
- Creates or updates wood types
- Handles duplicate names (updates if exists)
- Color-coded output
- Summary statistics
- Error handling

**Usage:**
```bash
python manage.py populate_wood_types
```

## Adding Custom Wood Types

### Via Admin Interface
1. Login to admin
2. Go to Round Wood Purchasing > Wood types
3. Click "Add Wood type"
4. Fill in details
5. Save

### Via Script
Create a file `custom_wood_types.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
django.setup()

from app_round_wood.models import WoodType

custom_woods = [
    {
        'name': 'Custom Oak',
        'species': 'hardwood',
        'default_diameter_inches': 14.0,
        'default_length_feet': 18.0,
        'description': 'Custom oak specification'
    },
]

for data in custom_woods:
    WoodType.objects.create(**data)
    print(f"Created: {data['name']}")
```

Run it:
```bash
python custom_wood_types.py
```

## Dimensions Reference

### Standard Log Sizes

| Wood Type | Diameter (inches) | Length (feet) | Use Case |
|-----------|-------------------|---------------|----------|
| Oak | 12 | 16 | Furniture |
| Pine | 10 | 16 | Construction |
| Maple | 10 | 12 | Flooring |
| Walnut | 12 | 14 | Fine furniture |
| Cedar | 8 | 12 | Outdoor |
| Teak | 14 | 12 | Marine |

Note: These are defaults; individual orders can override these values.

## Volume Calculation

The system calculates log volume using:

```
Volume (cubic feet) = (π × (diameter/2)²  × length × 12) / 1728
```

With these defaults, volumes are automatically calculated when creating purchase order items.

## Best Practices

1. **Standardize Naming**: Use consistent naming (e.g., "Oak Logs" not "Oak" or "Oak Log")
2. **Keep Descriptions Detailed**: Help users understand use cases
3. **Set Realistic Defaults**: Use average dimensions for each wood type
4. **Update Regularly**: Review and update wood types quarterly
5. **Archive Unused Types**: Set `is_active=False` instead of deleting

## Troubleshooting

### Command Not Found
```bash
python manage.py populate_wood_types
# Error: Unknown command 'populate_wood_types'
```

**Solution:** Ensure Django app is in INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'app_round_wood',
    ...
]
```

### Database Errors
```bash
# Run migrations first
python manage.py migrate app_round_wood
```

### Duplicate Entry Error
The management command uses `update_or_create`, so running it multiple times is safe.

## Statistics

- **Total Wood Types**: 15
- **Hardwoods**: 8
- **Softwoods**: 5
- **Tropical Woods**: 2
- **Population Date**: 2024
- **Last Updated**: 2024

## Future Enhancements

1. Bulk import from CSV file
2. Wood type categorization/hierarchy
3. Seasonal availability tracking
4. Quality grades per wood type
5. Environmental certifications (FSC, PEFC)
6. Price history per wood type
7. Supplier mappings

---

**Document**: WOOD_TYPES_POPULATION_GUIDE.md
**Status**: Complete
**Module**: Round Wood Purchasing System

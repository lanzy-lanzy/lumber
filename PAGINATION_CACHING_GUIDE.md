# Products List - Pagination & Caching Implementation

## Overview
The products list now features server-side pagination and API-level caching for significantly faster load times and better performance.

## Features Implemented

### 1. **Server-Side Pagination**
- **Page Size**: 20 products per page
- **Configurable**: Supports `page_size` parameter in API requests
- **Max Page Size**: 100 products (security limit)
- **Location**: `/api/products/?page=1&page_size=20`

### 2. **Caching Strategy**
- **Cache Backend**: In-Memory (LocMemCache) for development
- **Cache Duration**: 
  - Product Lists: 5 minutes (300 seconds)
  - Individual Products: 10 minutes (600 seconds)
- **Auto-Invalidation**: Cache clears on create/update/delete operations

### 3. **Frontend UI Enhancements**
- **Pagination Controls**: Previous/Next buttons + numbered page buttons
- **Results Info**: Shows "Showing X to Y of Z products"
- **Loading Indicator**: Animated spinner during data fetch
- **Smart Page Navigation**: Max 5 visible page buttons

### 4. **Performance Optimizations**
- **Database Optimization**: 
  - `select_related('category')` - Reduces N+1 queries
  - `prefetch_related('inventory')` - Optimizes reverse relations
- **API Response Caching**: 
  - Caches based on URL parameters (page, page_size, filters)
  - Separate cache keys for list vs detail endpoints

## API Endpoints

### Get Products List (Paginated)
```
GET /api/products/?page=1&page_size=20
```

**Response**:
```json
{
  "count": 15,
  "next": "http://localhost:8000/api/products/?page=2&page_size=20",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Red Oak 1x4x8",
      "sku": "RO-1x4-8",
      "category": 1,
      "thickness": "0.75",
      "width": "3.50",
      "length": "8.00",
      "price_per_board_foot": "8.50",
      "price_per_piece": "18.00",
      "image": "https://...",
      "is_active": true,
      "inventory": {
        "quantity_pieces": 45,
        "total_board_feet": "270.00"
      },
      "created_at": "2024-...",
      "updated_at": "2024-..."
    }
  ]
}
```

### Get Individual Product
```
GET /api/products/{id}/
```

## Frontend Implementation

### Data States
```javascript
{
  products: [],              // Current page products
  currentPage: 1,           // Current page number
  pageSize: 20,             // Items per page
  totalProducts: 0,         // Total count from API
  totalPages: 1,            // Calculated from total
  isLoading: false,         // Loading state
  filteredProducts: [],     // Client-side filtered results
}
```

### Key Methods
- `loadProducts(page)` - Fetch products with pagination
- `goToPage(page)` - Navigate to specific page
- `filterProducts()` - Client-side filtering (resets to page 1)

## Configuration Files

### settings.py
```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        "OPTIONS": {
            "MAX_ENTRIES": 1000
        }
    }
}
```

### Cache Clearing on Mutations
- **POST** (Create): Clears `products_list_*` cache
- **PUT/PATCH** (Update): Clears all product caches
- **DELETE**: Clears all product caches

## Performance Metrics

### Before Pagination/Caching
- Load all 15 products on every request
- No caching - full DB queries
- Single large response

### After Pagination/Caching
- Load 20 products per page
- 5-minute cache for repeated requests
- Optimized DB queries (select_related + prefetch_related)
- Reduced network payload

## Usage Examples

### Load First Page
```javascript
await loadProducts(1);
```

### Load Specific Page
```javascript
goToPage(3);
```

### Change Page Size (in HTML)
```html
<select x-model.number="pageSize" @change="loadProducts(1)">
  <option value="10">10 per page</option>
  <option value="20" selected>20 per page</option>
  <option value="50">50 per page</option>
</select>
```

## Cache Invalidation Scenarios

| Action | Cache Cleared |
|--------|--------------|
| Add Product | `products_list_*` |
| Edit Product | All product caches |
| Delete Product | All product caches |
| Manual page load | Previous cache expires (5 min) |

## Production Recommendations

### 1. Switch to Redis Cache
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

### 2. Increase Cache Duration
- Production: 15-30 minutes for product lists
- Still clear on mutations

### 3. Add Cache Headers
```python
from django.views.decorators.http import condition
```

### 4. Database Indexes
- Already indexed: `sku`, `category`
- Consider adding: `(category, is_active, created_at)`

## Troubleshooting

### Cache Not Clearing
- Check if mutation endpoints are clearing cache
- Use `python manage.py shell` to manually clear:
  ```python
  from django.core.cache import cache
  cache.clear()
  ```

### Pagination Not Working
- Verify DRF pagination in settings
- Check API response has `count`, `results`, `next`, `previous`

### Loading Indicator Stuck
- Check browser console for errors
- Verify API endpoint is accessible
- Check network tab for failed requests

# Shopping Cart API Reference

## Base URL
```
http://localhost:8000/api/cart/
```

## Authentication
All endpoints require a valid authentication token in the header:
```
Authorization: Bearer YOUR_TOKEN
```

## Endpoints

### 1. Get My Cart

**GET** `/api/cart/my_cart/`

Returns the current user's shopping cart with all items.

#### Response (200 OK)
```json
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product_id": 25,
      "product": 25,
      "product_name": "2x12 LVL Beam",
      "product_sku": "SKU-001",
      "product_image": "/media/products/lumber1.jpg",
      "quantity": 5,
      "price": 7.25,
      "subtotal": 36.25,
      "available_quantity": 100,
      "added_at": "2024-12-12T10:30:00Z",
      "updated_at": "2024-12-12T10:35:00Z"
    }
  ],
  "total": 36.25,
  "total_items": 5,
  "item_count": 1,
  "created_at": "2024-12-12T09:00:00Z",
  "updated_at": "2024-12-12T10:35:00Z"
}
```

**Fields:**
- `id`: Cart ID
- `items`: Array of cart items
- `total`: Total price of all items in cart
- `total_items`: Total quantity of items (sum of quantities)
- `item_count`: Number of unique products in cart
- `created_at`: When cart was created
- `updated_at`: Last update timestamp

---

### 2. Add Item to Cart

**POST** `/api/cart/add_item/`

Adds a new item to cart or increases quantity if item already exists.

#### Request Body
```json
{
  "product_id": 25,
  "quantity": 5
}
```

**Required Fields:**
- `product_id`: Integer, ID of product to add
- `quantity`: Integer, number of pieces to add (default: 1)

#### Response (201 Created)
```json
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product_id": 25,
      "product": 25,
      "product_name": "2x12 LVL Beam",
      "product_sku": "SKU-001",
      "product_image": "/media/products/lumber1.jpg",
      "quantity": 5,
      "price": 7.25,
      "subtotal": 36.25,
      "available_quantity": 100,
      "added_at": "2024-12-12T10:30:00Z",
      "updated_at": "2024-12-12T10:30:00Z"
    }
  ],
  "total": 36.25,
  "total_items": 5,
  "item_count": 1,
  "created_at": "2024-12-12T09:00:00Z",
  "updated_at": "2024-12-12T10:30:00Z"
}
```

#### Error Responses

**400 Bad Request** - Missing product_id
```json
{
  "error": "product_id is required"
}
```

**400 Bad Request** - Invalid quantity
```json
{
  "error": "quantity must be at least 1"
}
```

**400 Bad Request** - Insufficient stock
```json
{
  "error": "Insufficient stock. Available: 10"
}
```

**404 Not Found** - Product doesn't exist
```json
{
  "error": "Product not found"
}
```

---

### 3. Update Item Quantity

**POST** `/api/cart/update_item/`

Updates the quantity of an existing cart item. Setting quantity to 0 removes the item.

#### Request Body
```json
{
  "item_id": 1,
  "quantity": 10
}
```

**Required Fields:**
- `item_id`: Integer, ID of cart item to update
- `quantity`: Integer, new quantity (0 = remove)

#### Response (200 OK)
```json
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product_id": 25,
      "product": 25,
      "product_name": "2x12 LVL Beam",
      "product_sku": "SKU-001",
      "product_image": "/media/products/lumber1.jpg",
      "quantity": 10,
      "price": 7.25,
      "subtotal": 72.50,
      "available_quantity": 100,
      "added_at": "2024-12-12T10:30:00Z",
      "updated_at": "2024-12-12T10:45:00Z"
    }
  ],
  "total": 72.50,
  "total_items": 10,
  "item_count": 1,
  "created_at": "2024-12-12T09:00:00Z",
  "updated_at": "2024-12-12T10:45:00Z"
}
```

#### Error Responses

**400 Bad Request** - Missing parameters
```json
{
  "error": "item_id and quantity are required"
}
```

**400 Bad Request** - Insufficient stock
```json
{
  "error": "Insufficient stock. Available: 5"
}
```

**404 Not Found** - Item not in cart
```json
{
  "error": "Cart item not found"
}
```

---

### 4. Remove Item from Cart

**POST** `/api/cart/remove_item/`

Removes a specific item from the cart.

#### Request Body
```json
{
  "item_id": 1
}
```

**Required Fields:**
- `item_id`: Integer, ID of cart item to remove

#### Response (200 OK)
```json
{
  "id": 1,
  "items": [],
  "total": 0.0,
  "total_items": 0,
  "item_count": 0,
  "created_at": "2024-12-12T09:00:00Z",
  "updated_at": "2024-12-12T10:50:00Z"
}
```

#### Error Responses

**400 Bad Request** - Missing item_id
```json
{
  "error": "item_id is required"
}
```

**404 Not Found** - Item not in cart
```json
{
  "error": "Cart item not found"
}
```

---

### 5. Clear Cart

**POST** `/api/cart/clear_cart/`

Removes all items from the cart.

#### Request Body
```json
{}
```

No parameters required.

#### Response (200 OK)
```json
{
  "id": 1,
  "items": [],
  "total": 0.0,
  "total_items": 0,
  "item_count": 0,
  "created_at": "2024-12-12T09:00:00Z",
  "updated_at": "2024-12-12T10:55:00Z"
}
```

---

### 6. Checkout (Create Order)

**POST** `/api/cart/checkout/`

Creates a sales order from all items in the cart and clears the cart.

#### Request Body
```json
{
  "payment_type": "partial"
}
```

**Optional Fields:**
- `payment_type`: String, one of: "cash", "partial", "credit" (default: "cash")

#### Response (201 Created)
```json
{
  "id": 15,
  "so_number": "SO-2024-001",
  "customer": 3,
  "customer_name": "John Doe",
  "total_amount": "100.50",
  "discount": "20.00",
  "discount_amount": "20.10",
  "payment_type": "partial",
  "amount_paid": "0.00",
  "balance": "80.40",
  "notes": "",
  "sales_order_items": [
    {
      "id": 1,
      "sales_order": 15,
      "product": 25,
      "product_name": "2x12 LVL Beam",
      "quantity_pieces": 5,
      "board_feet": "20.00",
      "unit_price": "7.25",
      "subtotal": "36.25"
    },
    {
      "id": 2,
      "sales_order": 15,
      "product": 26,
      "product_name": "Glulam Beam",
      "quantity_pieces": 8,
      "board_feet": "32.00",
      "unit_price": "7.25",
      "subtotal": "58.00"
    }
  ],
  "created_by": 2,
  "created_by_name": "Admin User",
  "created_at": "2024-12-12T11:00:00Z",
  "updated_at": "2024-12-12T11:00:00Z"
}
```

#### Error Responses

**400 Bad Request** - Cart is empty
```json
{
  "error": "Cart is empty"
}
```

**400 Bad Request** - Stock validation failed
```json
{
  "error": "Insufficient stock for product: 2x12 LVL Beam"
}
```

**404 Not Found** - Cart not found
```json
{
  "error": "Cart not found"
}
```

**400 Bad Request** - Invalid payment type
```json
{
  "error": "Invalid payment_type"
}
```

---

## Example Workflows

### Workflow 1: Add Product and Checkout

```bash
# 1. Get current cart
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/cart/my_cart/

# 2. Add item to cart
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"product_id": 25, "quantity": 5}' \
  http://localhost:8000/api/cart/add_item/

# 3. Check cart
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/cart/my_cart/

# 4. Checkout
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"payment_type": "partial"}' \
  http://localhost:8000/api/cart/checkout/
```

### Workflow 2: Update Multiple Items

```bash
# 1. Add first item
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"product_id": 25, "quantity": 5}' \
  http://localhost:8000/api/cart/add_item/

# 2. Add second item
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"product_id": 26, "quantity": 8}' \
  http://localhost:8000/api/cart/add_item/

# 3. Update first item quantity
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"item_id": 1, "quantity": 10}' \
  http://localhost:8000/api/cart/update_item/

# 4. Remove second item
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"item_id": 2}' \
  http://localhost:8000/api/cart/remove_item/
```

## Response Format

All successful responses return:
- **Status Code**: 200 (for GET/updates) or 201 (for POST that creates)
- **Content-Type**: application/json
- **Body**: JSON object with requested data

All error responses return:
- **Status Code**: 400 (bad request), 404 (not found), or 500 (server error)
- **Content-Type**: application/json
- **Body**: JSON object with "error" field describing the problem

## Rate Limiting
No rate limiting currently implemented. All authenticated users can make unlimited requests.

## Pagination
Not applicable - cart data is always returned in full.

## Caching
Cart data is fresh on each request. No caching is used.

## Data Types

- **Integers**: product_id, item_id, quantity, available_quantity
- **Decimals**: price, subtotal, total, total_amount, balance (returned as strings)
- **Strings**: product_name, product_sku, product_image, payment_type
- **Booleans**: None currently
- **Timestamps**: ISO 8601 format (e.g., "2024-12-12T10:30:00Z")

## Currency
All prices are in Philippine Peso (₱) with 2 decimal places.

## Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing or invalid token |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error - Server error occurred |

# Shopping Cart Flow Diagram

## Database Schema

```
┌─────────────────────────────────────────────────────────────┐
│                     Core Architecture                        │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌───────────────────────┐
│   CustomUser     │         │  LumberProduct        │
│  (auth.User)     │         │  (app_inventory)      │
├──────────────────┤         ├───────────────────────┤
│ id (PK)          │         │ id (PK)               │
│ username         │         │ name                  │
│ email            │         │ sku                   │
│ first_name       │         │ price_per_board_foot │
│ last_name        │         │ board_feet            │
│ password         │         │ image                 │
└──────────────────┘         │ is_active             │
        ▲                     └───────────────────────┘
        │ 1                              ▲
        │                                │
   ┌────┴─────────────────────────────────┴──────┐
   │                                              │
   │        ┌──────────────────────────┐         │
   │        │   ShoppingCart (NEW)     │         │
   │        ├──────────────────────────┤         │
   │        │ id (PK)                  │         │
   ├────────┤ user_id (FK to User)     │         │
   │        │ created_at               │         │
   │        │ updated_at               │         │
   │        └──────────────────────────┘         │
   │                  │ 1:N                       │
   │                  │                          │
   │        ┌─────────▼──────────────────────┐   │
   │        │  CartItem (NEW)                │   │
   │        ├────────────────────────────────┤   │
   │        │ id (PK)                        │   │
   │        │ cart_id (FK to ShoppingCart)   │   │
   │        │ product_id (FK to Product)─────┼───┘
   │        │ quantity                       │
   │        │ added_at                       │
   │        │ updated_at                     │
   │        │ UNIQUE(cart, product)          │
   │        └────────────────────────────────┘
   │
   │
   └─────────────────────────────────────────┐
                                             │
        ┌──────────────────────────────────────┴─────┐
        │                                            │
        │      ┌─────────────────────────┐          │
        │      │   SalesOrder            │          │
        │      ├─────────────────────────┤          │
        │      │ id (PK)                 │          │
        │      │ so_number               │          │
        │      │ customer_id (FK)        │          │
        ├──────┤ total_amount            │          │
        │      │ payment_type            │          │
        │      │ amount_paid             │          │
        │      │ created_by_id           │          │
        │      └─────────────────────────┘          │
        │               │ 1:N                       │
        │               │                          │
        │      ┌────────▼──────────────────┐      │
        │      │  SalesOrderItem          │      │
        │      ├───────────────────────────┤      │
        │      │ id (PK)                   │      │
        │      │ sales_order_id            │      │
        │      │ product_id (FK)───────────┼──────┘
        │      │ quantity_pieces           │
        │      │ unit_price                │
        │      │ subtotal                  │
        │      └───────────────────────────┘
        │
        └──────────────────────────────────────┐
                                               │
                    ┌──────────────────────────┴──┐
                    │                             │
            ┌───────▼────────────┐       ┌────────▼────────┐
            │    Customer        │       │    Receipt      │
            │  (app_sales)       │       │  (app_sales)    │
            ├────────────────────┤       ├─────────────────┤
            │ id (PK)            │       │ id (PK)         │
            │ name               │       │ receipt_number  │
            │ email              │       │ sales_order_id  │
            │ phone              │       │ amount_tendered │
            │ address            │       │ change          │
            │ is_senior          │       │ created_at      │
            │ is_pwd             │       └─────────────────┘
            └────────────────────┘
```

## User Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   CUSTOMER SHOPPING FLOW                      │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │  Customer Login  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Customer Portal  │
                    │   Dashboard      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Browse Products  │
                    │ /customer/       │
                    │ products/        │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  View Product    │
                    │  Details         │
                    │  /customer/      │
                    │  products/[id]/  │
                    └────────┬─────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
         ┌──────▼─────┐         ┌────────▼────────┐
         │ Add More   │         │  Add to Cart    │
         │ Products   │         │  POST /api/     │
         │            │         │  cart/add_item/ │
         └──────┬─────┘         └────────┬────────┘
                │                        │
                │              ┌─────────▼────────┐
                │              │  ✓ Item Added    │
                │              │  (real-time      │
                │              │   feedback)      │
                │              └─────────┬────────┘
                │                        │
                └────────┬───────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │ View Shopping Cart         │
            │ /customer/cart/            │
            │ GET /api/cart/my_cart/     │
            └────────────┬───────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    ┌───▼──┐      ┌──────▼──────┐    ┌───▼──────┐
    │ Edit │      │   Proceed   │    │  Clear   │
    │Qty   │      │   Checkout  │    │   Cart   │
    └───┬──┘      └──────┬──────┘    └──────────┘
        │                │
        │                ▼
    ┌───▼──────────────────────────┐
    │  POST /api/cart/checkout/    │
    └───┬──────────────────────────┘
        │
        ▼
    ┌──────────────────────┐
    │ ✓ Order Created      │
    │ (SalesOrder)         │
    │ Order #: SO-2024-001 │
    └───┬──────────────────┘
        │
        ▼
    ┌──────────────────────┐
    │ View Order Details   │
    │ /customer/orders/    │
    │ [order_id]/          │
    └──────────────────────┘
```

## API Call Flow

```
┌──────────────────────────────────────────────────────────────┐
│                      API ENDPOINTS                             │
└──────────────────────────────────────────────────────────────┘

CLIENT (Frontend - Browser)
    │
    ├─► GET /api/cart/my_cart/ ──────────────────┐
    │                                              │
    │   Response: { items: [...], total: 100 }   │
    │◄─────────────────────────────────────────────┤
    │                                              │
    │                                              ▼
    ├─► POST /api/cart/add_item/ ─────────┐      BACKEND
    │   { product_id: 25, qty: 5 }        │      (Django REST)
    │◄─ Response: Updated cart ──────────┘
    │
    │
    ├─► POST /api/cart/update_item/
    │   { item_id: 1, quantity: 10 }
    │◄─ Response: Updated cart
    │
    │
    ├─► POST /api/cart/remove_item/
    │   { item_id: 1 }
    │◄─ Response: Updated cart
    │
    │
    ├─► POST /api/cart/clear_cart/
    │   {}
    │◄─ Response: Empty cart
    │
    │
    ├─► POST /api/cart/checkout/ ───────────┐
    │   { payment_type: "partial" }         │
    │◄─ Response: SalesOrder object ────────┼─────► Creates:
    │                                        │  • Sales Order
    │                                        │  • Order Items
    │                                        │  • Apply Discounts
    │                                        │  • Clear Cart
```

## State Transitions

```
┌─────────────────────────────────────────────────────────────┐
│              CART ITEM STATE TRANSITIONS                      │
└─────────────────────────────────────────────────────────────┘

                    START
                     │
                     ▼
            ┌────────────────┐
            │  Cart Empty    │
            └────────┬───────┘
                     │
         add_item()  │
                     ▼
            ┌────────────────────┐
            │ Item in Cart       │
            │ qty=5, price=$7.25 │
            └────┬───────────────┘
                 │
         ┌───────┼───────┐
         │               │
    update_qty()  remove_item()
         │               │
         │       ┌───────▼──────┐
         │       │ Item Removed │
         │       └──────────────┘
         │
         ▼
    ┌────────────────────┐
    │ Item Updated       │
    │ qty=10, price=$7.25│
    └────────┬───────────┘
             │
         checkout()
             │
             ▼
    ┌──────────────────────┐
    │ Order Created        │
    │ Cart Cleared         │
    └──────────────────────┘
```

## Frontend Component Flow

```
┌──────────────────────────────────────────────────────────────┐
│              FRONTEND COMPONENT HIERARCHY                      │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ Product Detail Page                              │
│ (/customer/products/[id]/)                       │
├──────────────────────────────────────────────────┤
│ ┌────────────────────────────────────────────┐  │
│ │ Product Image                              │  │
│ └────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────┐  │
│ │ Product Name, SKU, Price                   │  │
│ └────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────┐  │
│ │ Quantity Selector (NEW)                    │  │
│ │  [-] [5] [+]  Max: 100 pieces              │  │
│ └────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────┐  │
│ │ [Add to Cart] [Continue Shopping]          │  │
│ │  (JS: addToCart(productId))                │  │
│ └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────┐
│ Shopping Cart Page (NEW)                         │
│ (/customer/cart/)                                │
├──────────────────────────────────────────────────┤
│                                                  │
│ ┌──────────────────────┐  ┌────────────────────┐│
│ │ Cart Items Section   │  │ Order Summary      ││
│ ├──────────────────────┤  ├────────────────────┤│
│ │ ┌────────────────┐   │  │ Items: 5           ││
│ │ │ [Image]Product1│   │  │ Subtotal: ₱100.00  ││
│ │ │ Qty: 5  Price: │   │  │                    ││
│ │ │ [-] 5 [+]     │   │  │ [Checkout]         ││
│ │ │ Subtotal: $X   │   │  │ [Clear Cart]       ││
│ │ │ [Remove]       │   │  │ [Continue Shop]    ││
│ │ └────────────────┘   │  │                    ││
│ │                      │  │                    ││
│ │ ┌────────────────┐   │  └────────────────────┘│
│ │ │ [Image]Product2│   │                        │
│ │ │ Qty: 8         │   │  (JS functions:)       │
│ │ │ [-] 8 [+]     │   │  • loadCart()          │
│ │ │ Subtotal: $Y   │   │  • renderCart()        │
│ │ │ [Remove]       │   │  • updateQuantity()    │
│ │ └────────────────┘   │  • removeItem()        │
│ │                      │  • clearCart()         │
│ └──────────────────────┘  • proceedCheckout()   │
│                                                  │
└──────────────────────────────────────────────────┘
```

## Data Flow Sequence

```
┌──────────────────────────────────────────────────────────────┐
│         CHECKOUT SEQUENCE DIAGRAM                             │
└──────────────────────────────────────────────────────────────┘

Customer                Browser              API                Database
    │                     │                  │                    │
    │  Click Checkout     │                  │                    │
    ├────────────────────►│                  │                    │
    │                     │  POST /checkout/ │                    │
    │                     ├─────────────────►│                    │
    │                     │                  │ Get Cart Items     │
    │                     │                  ├───────────────────►│
    │                     │                  │◄─── Cart Data ─────┤
    │                     │                  │                    │
    │                     │                  │ Validate Stock     │
    │                     │                  │ for Each Item      │
    │                     │                  │                    │
    │                     │                  │ Get/Create         │
    │                     │                  │ Customer           │
    │                     │                  ├───────────────────►│
    │                     │                  │◄── Customer ID ────┤
    │                     │                  │                    │
    │                     │                  │ Create SalesOrder  │
    │                     │                  ├───────────────────►│
    │                     │                  │                    │
    │                     │                  │ Create OrderItems  │
    │                     │                  ├───────────────────►│
    │                     │                  │                    │
    │                     │                  │ Update Inventory   │
    │                     │                  ├───────────────────►│
    │                     │                  │                    │
    │                     │                  │ Clear Cart Items   │
    │                     │                  ├───────────────────►│
    │                     │                  │◄─ Success ─────────┤
    │                     │◄─ SalesOrder ────┤                    │
    │◄─────Redirect───────┤                  │                    │
    │  /orders/[id]/      │                  │                    │
    │                     │                  │                    │
```

## Error Handling Flow

```
┌──────────────────────────────────────────────────────────────┐
│          ERROR HANDLING PATHS                                  │
└──────────────────────────────────────────────────────────────┘

User Action
    │
    ├─► Add Invalid Qty
    │       └─► Error: "Invalid quantity"
    │           └─► Alert User
    │
    ├─► Product Out of Stock
    │       └─► Error: "Insufficient stock. Available: 0"
    │           └─► Prevent Add
    │
    ├─► Cart Checkout with Empty Cart
    │       └─► Error: "Cart is empty"
    │           └─► Block Checkout
    │
    ├─► Product No Longer Active
    │       └─► Error: "Product not found"
    │           └─► Item Can't be Added
    │
    └─► Stock Reduced Before Checkout
            └─► Error During Checkout
                └─► Notify & Refresh
```

## Performance Notes

```
Cart Load Time: ~200-300ms
  - GET /api/cart/my_cart/ includes all items with prices

Add to Cart: ~150-250ms
  - POST /api/cart/add_item/ with validation

Checkout: ~500-800ms
  - POST /api/cart/checkout/ creates order with multiple items
  - Includes inventory updates

Auto-refresh: Every 5 seconds
  - Keeps cart data fresh
  - Can be configured in template
```

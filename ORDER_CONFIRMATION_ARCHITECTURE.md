# Order Confirmation System - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CUSTOMER INTERFACE LAYER                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Dashboard Template                                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ {% include 'order_notifications.html' %}                 │   │
│  │                                                           │   │
│  │ ┌─────────────────────────────────────────────────────┐  │   │
│  │ │ Alert: "3 New Notifications"  [View Details]       │  │   │
│  │ └─────────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  │ ┌─────────────────────────────────────────────────────┐  │   │
│  │ │ Ready for Pickup Alert                             │  │   │
│  │ │                                                     │  │   │
│  │ │ Order #SO-001: Ready ✓                             │  │   │
│  │ │ Amount: ₱1,500.00 | Balance: ₱0.00 | Paid ✓       │  │   │
│  │ │ [View Order]                                        │  │   │
│  │ └─────────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  │ ┌─────────────────────────────────────────────────────┐  │   │
│  │ │ Notification Panel (Collapsible)                    │  │   │
│  │ │ ────────────────────────────────────────────────    │  │   │
│  │ │ "Order Confirmed"                                  │  │   │
│  │ │ Your order SO-001 has been created...              │  │   │
│  │ │ 2 hours ago                                         │  │   │
│  │ │                                                     │  │   │
│  │ │ "Ready for Pickup" [Mark as Read]                 │  │   │
│  │ │ Your order is now ready...                         │  │   │
│  │ │ 1 hour ago                                         │  │   │
│  │ └─────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
         ┌────────────────────────────────────────┐
         │   Context Processor                    │
         │   order_notifications()                │
         │                                        │
         │ GET: notifications                     │
         │ GET: notification_count                │
         │ GET: ready_pickups                     │
         │ GET: pending_orders                    │
         └────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    API ENDPOINTS LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  OrderConfirmationViewSet              NotificationViewSet       │
│  ┌──────────────────────────────────┐  ┌──────────────────────┐  │
│  │ POST create_confirmation/        │  │ GET my_notifications/│  │
│  │ POST mark_ready/                 │  │ POST mark_as_read/   │  │
│  │ POST mark_payment_received/      │  │ POST mark_all_as_read│  │
│  │ POST mark_picked_up/             │  │ GET unread_count/    │  │
│  │ GET pending_pickups/             │  └──────────────────────┘  │
│  └──────────────────────────────────┘                             │
│                      ↓                                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  OrderConfirmationService                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ create_order_confirmation(order_id, pickup_date, user)   │   │
│  │  → Creates OrderConfirmation record                       │   │
│  │  → Creates "order_confirmed" notification                │   │
│  │                                                           │   │
│  │ confirm_order_ready(order_id)                            │   │
│  │  → Sets status="ready_for_pickup"                        │   │
│  │  → Sets ready_at timestamp                               │   │
│  │  → Creates "ready_for_pickup" notification              │   │
│  │                                                           │   │
│  │ mark_payment_received(order_id)                          │   │
│  │  → Sets is_payment_complete=True                         │   │
│  │  → Sets payment_completed_at timestamp                   │   │
│  │  → Creates "payment_completed" notification             │   │
│  │                                                           │   │
│  │ mark_order_picked_up(order_id)                           │   │
│  │  → Sets status="picked_up"                               │   │
│  │  → Sets picked_up_at timestamp                           │   │
│  │  → Creates "order_picked_up" notification               │   │
│  │                                                           │   │
│  │ get_customer_pending_pickups(customer_id)                │   │
│  │  → Returns orders ready for pickup                       │   │
│  │                                                           │   │
│  │ get_customer_notifications(customer_id)                  │   │
│  │  → Returns unread notifications for customer             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                      ↓                                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   DATABASE LAYER                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  OrderConfirmation                   OrderNotification            │
│  ┌────────────────────────────────┐  ┌──────────────────────────┐│
│  │ id                             │  │ id                       ││
│  │ sales_order_id (1-to-1)        │  │ sales_order_id (FK)      ││
│  │ customer_id (FK)               │  │ customer_id (FK)         ││
│  │ status                         │  │ notification_type        ││
│  │ is_payment_complete            │  │ title                    ││
│  │ estimated_pickup_date          │  │ message                  ││
│  │ actual_pickup_date             │  │ is_read                  ││
│  │ confirmed_at                   │  │ read_at                  ││
│  │ ready_at                       │  │ created_at               ││
│  │ picked_up_at                   │  │ updated_at               ││
│  │ payment_completed_at           │  └──────────────────────────┘│
│  │ notes                          │                              │
│  │ created_by_id (FK)             │  Indexes:                   │
│  │ created_at                     │  - (customer_id, -created_at)│
│  │ updated_at                     │  - (is_read, -created_at)   │
│  │ updated_by_id (FK)             │  - (notification_type, -date)│
│  │                                │                              │
│  │ Indexes:                       │                              │
│  │ - (customer_id, -created_at)   │                              │
│  │ - (status, -created_at)        │                              │
│  └────────────────────────────────┘                              │
│                                                                   │
│  Related to SalesOrder (1-to-1)    Related to Customer (many-to-1)│
│  Related to Customer (FK)           Related to SalesOrder (FK)    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                         SALES ORDER CREATION                        │
└────────────────────────────────────────────────────────────────────┘
                              ↓
                   SalesService.create_order()
                              ↓
                        ┌─────────────┐
                        │ SalesOrder  │
                        │ created     │
                        └─────────────┘
                              ↓
        OrderConfirmationService.create_order_confirmation()
                              ↓
              ┌───────────────────────────────┐
              ↓                               ↓
      ┌──────────────────┐        ┌────────────────────┐
      │  OrderConfirm    │        │ OrderNotification  │
      │  status: created │        │ type: order_confirm│
      │  confirmed_at: ∅ │        │ is_read: false     │
      │  ready_at: ∅     │        │ created_at: now    │
      └──────────────────┘        └────────────────────┘
              ↓                               ↓
         Admin sees                    Customer sees
         in Django Admin               in Dashboard
                              ↓
        ┌────────────────────────────────────────────┐
        │   Admin marks order as ready to pickup     │
        └────────────────────────────────────────────┘
                              ↓
        OrderConfirmationService.confirm_order_ready()
                              ↓
        ┌───────────────────────────────────────────┐
        ↓                                           ↓
┌──────────────────────┐            ┌────────────────────────┐
│ OrderConfirm updated │            │ OrderNotification NEW  │
│ status: ready_pickup │            │ type: ready_for_pickup │
│ ready_at: now        │            │ is_read: false         │
│ is_payment_complete: │            │ title: "Ready..."      │
│   (depends on payment)             │ created_at: now        │
└──────────────────────┘            └────────────────────────┘
        ↓                                           ↓
   Admin sees status              Customer sees:
   updated in admin               - Alert: "Order Ready!"
                                  - Notification: unread
                                  - Balance due: shows if unpaid
                              ↓
        ┌────────────────────────────────────────────┐
        │   Admin records payment received           │
        └────────────────────────────────────────────┘
                              ↓
        OrderConfirmationService.mark_payment_received()
                              ↓
        ┌───────────────────────────────────────────┐
        ↓                                           ↓
┌──────────────────────┐            ┌────────────────────────┐
│ OrderConfirm updated │            │ OrderNotification NEW  │
│ is_payment_complete: │            │ type: payment_complete │
│   true               │            │ is_read: false         │
│ payment_completed_at:│            │ title: "Payment..."    │
│   now                │            │ created_at: now        │
└──────────────────────┘            └────────────────────────┘
        ↓                                           ↓
   Admin sees payment              Customer sees:
   marked in admin                 - Payment confirmed
                                   - Ready to pickup notification
                              ↓
        ┌────────────────────────────────────────────┐
        │   Customer picks up order                 │
        │   Admin records pickup                    │
        └────────────────────────────────────────────┘
                              ↓
        OrderConfirmationService.mark_order_picked_up()
                              ↓
        ┌───────────────────────────────────────────┐
        ↓                                           ↓
┌──────────────────────┐            ┌────────────────────────┐
│ OrderConfirm updated │            │ OrderNotification NEW  │
│ status: picked_up    │            │ type: order_picked_up  │
│ picked_up_at: now    │            │ is_read: false         │
└──────────────────────┘            └────────────────────────┘
        ↓                                           ↓
   Order marked complete          Customer sees:
   in admin                        - Thank you notification
                                   - Order removed from pending
                              ↓
                        ┌──────────────┐
                        │   COMPLETE   │
                        └──────────────┘
```

## Component Interaction Diagram

```
                    ┌─────────────┐
                    │   Customer  │
                    │   Browser   │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
   ┌─────────┐      ┌──────────┐      ┌─────────────┐
   │Dashboard │     │API Client│      │Admin Panel  │
   └────┬────┘      └────┬─────┘      └────┬────────┘
        │                │                  │
        │                │                  │
        └────────┬───────┴──────────────────┘
                 │
                 ↓ HTTP Requests
        ┌────────────────────────┐
        │  Django URL Router     │
        └────────┬───────────────┘
                 │
        ┌────────┴─────────────────┐
        │                          │
        ↓                          ↓
   ┌─────────────────┐     ┌────────────────────┐
   │ Template Views  │     │ API Views          │
   │ (customer.html) │     │ (ViewSets)         │
   └────────┬────────┘     └────────┬───────────┘
            │                       │
            ↓                       ↓
      ┌──────────────────┐    ┌──────────────────────────┐
      │ Context Processor│    │ OrderConfirmationViewSet │
      │ order_notif()    │    │ NotificationViewSet      │
      └────────┬─────────┘    └────────┬─────────────────┘
               │                      │
               └──────────┬───────────┘
                          │
                          ↓
                ┌──────────────────────┐
                │ OrderConfirmationServ│
                │ OrderConfirmationServ│ (Logic)
                └────────┬─────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ↓                                 ↓
┌──────────────────────────┐     ┌────────────────────┐
│ OrderConfirmation Model  │     │ OrderNotification  │
│ (Database queries)       │     │ Model              │
└──────────────────────────┘     └────────────────────┘
        │                                 │
        └────────────────┬────────────────┘
                         │
                         ↓
                  ┌──────────────┐
                  │   SQLite DB  │
                  │   (Tables)   │
                  └──────────────┘
```

## State Transition Diagram

```
                    ┌──────────┐
                    │  CREATED │ ← Initial state after order creation
                    └────┬─────┘
                         │
                         │ Admin action:
                         │ confirm_order()
                         │ or
                         │ Auto-confirm on creation
                         ↓
                    ┌──────────────┐
                    │  CONFIRMED   │
                    └────┬─────────┘
                         │
                         │ Admin action:
                         │ mark_ready_for_pickup()
                         │ (Requires warehouse to pick items)
                         ↓
              ┌──────────────────────┐
              │  READY FOR PICKUP ← ◇ Customer notification sent
              └────┬─────────────────┘
                   │
           ┌───────┴────────┐
           │                │
    Option A: Picked Up     Option B: Payment needed
           │                │
           ↓                ↓
    ┌──────────┐    ┌─────────────────┐
    │PICKED UP │    │ (waiting for $)  │
    │(Complete)│    └────────┬─────────┘
    └──────────┘             │
                     Admin records payment:
                     mark_payment_received()
                             │
                             ↓
                     ┌─────────────────┐
                     │ READY + PAID ← ◇ Notification sent
                     └────────┬────────┘
                              │
                     Customer picks up
                              │
                              ↓
                        ┌──────────┐
                        │ PICKED UP │
                        │(Complete) │
                        └──────────┘
                        
Alternative Path:
                    ┌──────────────┐
                    │     CREATED  │
                    └────┬─────────┘
                         │
                         │ Admin action:
                         │ cancel_order()
                         ↓
                    ┌──────────────┐
                    │   CANCELLED  │ ← Notification sent
                    │              │
                    └──────────────┘
```

## Notification Type Flow

```
                    ┌────────────────────────────────────┐
                    │     ORDER LIFECYCLE                │
                    └────────────────┬───────────────────┘
                                     │
     ┌───────────────────────────────┼───────────────────────────────┐
     │                               │                               │
     ↓                               ↓                               ↓
 ┌─────────────┐            ┌──────────────────┐          ┌─────────────┐
 │   CREATED   │            │   CONFIRMATION   │          │  CANCELLED  │
 │             │            │    PROCESS       │          │             │
 │ Event:      │            │                  │          │ Event:      │
 │ Order made  │            │ Event:           │          │ Cancellation│
 │             │            │ Admin confirms   │          │             │
 │ Notif:      │            │                  │          │ Notif:      │
 │ "Order      │            │ Notif:           │          │ "Order      │
 │ Confirmed"  │            │ "Order Ready..." │          │ Cancelled"  │
 └─────────────┘            └──────────────────┘          └─────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ↓                                 ↓
            ┌──────────────────┐           ┌──────────────────────┐
            │   PAYMENT FLOW   │           │    PICKUP FLOW       │
            │                  │           │                      │
            │ Event:           │           │ Event:               │
            │ Payment received │           │ Customer picks up    │
            │                  │           │                      │
            │ Notif:           │           │ Notif:               │
            │ "Payment         │           │ "Thank you for       │
            │ Received"        │           │ your order"          │
            └──────────────────┘           └──────────────────────┘
```

## Admin Workflow Diagram

```
┌────────────────────────────────────────────────────────────┐
│              DJANGO ADMIN INTERFACE                         │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  Sales → Sales Orders                                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Columns: SO#, Customer, Amount, Payment, Balance      │ │
│  │ Actions: [Mark as Ready for Pickup]                   │ │
│  │                                                        │ │
│  │ [SO-001] John Doe      ₱1,500      Cash      ₱0       │ │
│  │ [SO-002] Jane Smith    ₱2,000      Partial   ₱500     │ │
│  │ [SO-003] Bob Johnson   ₱3,000      Credit    ₱3,000   │ │
│  │                                                        │ │
│  │ [✓ Select] [▼ Action: Mark as Ready] [Go]            │ │
│  └────────────────────────────────────────────────────────┘ │
│                              ↓                                │
│                    (Bulk mark as ready)                       │
│                              ↓                                │
│  Sales → Order Confirmations                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Filter: Status ▼  Payment ▼  Date ▼                  │ │
│  │ Search: [Order #, Customer, Email]                    │ │
│  │                                                        │ │
│  │ SO#      Customer    Status        Paid?  Ready Since  │ │
│  │ SO-001   John Doe    Ready Pickup  ✓      13:45       │ │
│  │ SO-002   Jane Smith  Created       ✗      10:30       │ │
│  │ SO-003   Bob Johnson Ready Pickup  ✗      14:00       │ │
│  │                                                        │ │
│  │ [Click to edit]                                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                              ↓                                │
│        [Edit SO-001 Confirmation]                            │
│        ┌────────────────────────────────────────────────────┐│
│        │                                                    ││
│        │ Sales Order: SO-001 (read-only)                   ││
│        │ Customer: John Doe (read-only)                    ││
│        │ Status: [Ready for Pickup ▼]                      ││
│        │                                                    ││
│        │ Estimated Pickup: [12/20/2025]                    ││
│        │ Actual Pickup: [12/19/2025]                       ││
│        │                                                    ││
│        │ Payment Complete: [✓] Checked                     ││
│        │ Payment Completed At: 2025-12-13 15:45            ││
│        │                                                    ││
│        │ Timestamps:                                        ││
│        │ Confirmed: 2025-12-13 12:00                       ││
│        │ Ready At: 2025-12-13 13:45                        ││
│        │ Picked Up: 2025-12-19 10:00                       ││
│        │                                                    ││
│        │ Notes: [Order picked up successfully]             ││
│        │                                                    ││
│        │ [Save] [Save and Continue] [Delete]               ││
│        └────────────────────────────────────────────────────┘│
│                              ↓                                │
│  Sales → Order Notifications                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Filter: Type ▼  Read Status ▼  Date ▼                │ │
│  │ Search: [SO#, Customer, Title]                         │ │
│  │                                                        │ │
│  │ SO#      Customer    Type          Read? Sent         │ │
│  │ SO-001   John Doe    Ready Pickup  ✓     13:45       │ │
│  │ SO-001   John Doe    Order Created ✓     12:00       │ │
│  │ SO-002   Jane Smith  Order Created ✗     10:30       │ │
│  │ SO-003   Bob Johnson Ready Pickup  ✗     14:00       │ │
│  │                                                        │ │
│  │ [Click to view/edit]                                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

## Frontend Customer View Diagram

```
┌──────────────────────────────────────────────────────────────┐
│               CUSTOMER DASHBOARD                              │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ⚠️  3 New Notifications [View Details ▼]              │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ℹ️  Your Order is Ready for Pickup!                   │  │
│  │                                                        │  │
│  │ Order #SO-20251213-0001                   ✓ Ready    │  │
│  │ Ready since: Dec 13, 2025 1:45 PM                     │  │
│  │                                                        │  │
│  │ Total: ₱1,500.00 | Balance: ₱0.00 | ✓ Paid          │  │
│  │                                                        │  │
│  │ [View Order Details →]                                │  │
│  │                                                        │  │
│  │ Order #SO-20251212-0002                   ✓ Ready    │  │
│  │ Ready since: Dec 12, 2025 2:30 PM                     │  │
│  │                                                        │  │
│  │ Total: ₱2,000.00 | Balance: ₱500.00 | ✗ Unpaid      │  │
│  │                                                        │  │
│  │ [View Order Details →]                                │  │
│  │                                                        │  │
│  │ [×]                                                    │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                │
│  Notifications Panel                                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Recent Notifications                                    │ │
│  │                                                         │ │
│  │ ☐ Order #SO-20251213-0001 is Ready for Pickup!        │ │
│  │   [Order Ready for Pickup]                             │ │
│  │   Your order is now ready to pick up. Come collect it! │ │
│  │   2 hours ago                                     [Mark]│ │
│  │                                                         │ │
│  │ ✓ Payment Received for Order #SO-20251212-0002        │ │
│  │   [Payment Completed]                                  │ │
│  │   We've received your payment.                         │ │
│  │   1 day ago                                            │ │
│  │                                                         │ │
│  │ ✓ Order #SO-20251212-0001 Confirmed                   │ │
│  │   [Order Confirmed]                                    │ │
│  │   Your order has been created successfully.           │ │
│  │   2 days ago                                           │ │
│  │                                                         │ │
│  │ [View All Notifications →]                             │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                │
│  ─────────────────────────────────────────────────────────    │
│                    YOUR ORDERS                                 │
│  ─────────────────────────────────────────────────────────    │
│                                                                │
│  [Recent Orders listed below...]                              │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

This visual representation shows how all components interact to create a seamless order confirmation experience for customers.

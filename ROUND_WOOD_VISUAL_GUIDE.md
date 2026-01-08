# Round Wood Purchasing - Visual Guide & Diagrams

## 📊 System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                    ROUND WOOD PURCHASING SYSTEM                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐      │
│  │   Admin UI     │  │   REST API     │  │   Integrations   │      │
│  │                │  │                │  │                  │      │
│  │ • Create PO    │  │ 21 Endpoints   │  │ • Suppliers      │      │
│  │ • Inspect      │  │ • Search       │  │ • Inventory      │      │
│  │ • Track Status │  │ • Filter       │  │ • Reporting      │      │
│  │ • View Logs    │  │ • Sort         │  │ • Sales          │      │
│  └────────────────┘  └────────────────┘  └──────────────────┘      │
│           │                  │                      │               │
│           └──────────────────┼──────────────────────┘               │
│                              │                                      │
│                    ┌─────────▼────────────┐                        │
│                    │   ViewSets (6)       │                        │
│                    │   + Custom Actions   │                        │
│                    │   + Serializers      │                        │
│                    └─────────┬────────────┘                        │
│                              │                                      │
│                    ┌─────────▼────────────┐                        │
│                    │   Models (6)         │                        │
│                    │   + 100+ Fields      │                        │
│                    │   + 12 Indexes       │                        │
│                    └─────────┬────────────┘                        │
│                              │                                      │
│                    ┌─────────▼────────────┐                        │
│                    │   Database           │                        │
│                    │   (SQLite/PostgreSQL)│                        │
│                    └──────────────────────┘                        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Purchase Order Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PURCHASE ORDER LIFECYCLE                         │
└─────────────────────────────────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────────────┐
    │ PHASE 1: ORDER CREATION & APPROVAL                       │
    └────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │   DRAFT     │  ← Created by procurement team
    │             │  ← Add wood items
    │ Status      │  ← Calculate costs
    │ Ownership:  │  ← Ownership: PENDING
    │ PENDING     │
    └──────┬──────┘
           │ Submit order
           ↓
    ┌─────────────┐
    │ SUBMITTED   │  ← Awaiting approval
    │             │  ← Admin/Manager reviews
    │ Status      │  ← Supplier confirmed?
    │ Ownership:  │  ← Ownership: PENDING
    │ PENDING     │
    └──────┬──────┘
           │ Approve order
           ↓
    ┌─────────────┐
    │ CONFIRMED   │  ← Order approved
    │             │  ← Set delivery date
    │ Status      │  ← Cost locked
    │ Ownership:  │  ← Ownership: PENDING
    │ PENDING     │
    └─────────────┘

    ┌────────────────────────────────────────────────────────────┐
    │ PHASE 2: DELIVERY & OWNERSHIP TRANSFER                   │
    └────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ IN TRANSIT  │  ← Goods in transit
    │             │  ← Track shipment
    │ Status      │  ← Expected delivery date
    │ Ownership:  │
    │ PENDING     │
    └──────┬──────┘
           │ Goods delivered
           ↓
    ┌──────────────────┐
    │    DELIVERED     │  ← Physical delivery occurred
    │                  │  ← Record actual delivery date
    │ Status: DELIVERED│  ← Document delivery notes
    │ Ownership:       │  ← **OWNERSHIP TRANSFERS TO BUYER**
    │ TRANSFERRED ⭐   │
    └──────┬───────────┘
           │ Ownership now with lumber yard!

    ┌────────────────────────────────────────────────────────────┐
    │ PHASE 3: INSPECTION & QUALITY CONTROL                    │
    └────────────────────────────────────────────────────────────┘

    ┌──────────────────┐
    │  INSPECTING      │  ← Inspect each log batch
    │                  │  ← Check quality grade
    │ Status:DELIVERED │  ← Count acceptable/rejected
    │ Inspect: IN_PROG │  ← Document findings
    │ Ownership:       │  ← Identify issues
    │ TRANSFERRED      │
    └──────┬───────────┘
           │ Inspection passed
           ↓
    ┌──────────────────┐
    │    INSPECTED     │  ← All items passed
    │                  │  ← Quality verified
    │ Status:INSPECTED │  ← Inspector signed off
    │ Inspect: PASSED  │  ← Ready for stock-in
    │ Ownership:       │
    │ TRANSFERRED      │
    └──────┬───────────┘
           │ Ownership + Inspection passed
           │ → Can now stock in!

    ┌────────────────────────────────────────────────────────────┐
    │ PHASE 4: INVENTORY & FINAL CONFIRMATION                  │
    └────────────────────────────────────────────────────────────┘

    ┌──────────────────┐
    │     STOCKED      │  ← Auto-created in RoundWoodInventory
    │                  │  ← Created RoundWoodStockTransaction
    │ Status: STOCKED  │  ← Quantities & costs updated
    │ Inspect: PASSED  │  ← **OWNERSHIP CONFIRMED**
    │ Ownership:       │  ← Goods in warehouse
    │ CONFIRMED ⭐     │  ← Fully in possession
    └──────────────────┘
           ↓
       COMPLETE! ✅
       Ownership confirmed in inventory
       Ready for sales orders


    ┌────────────────────────────────────────────────────────────┐
    │ PHASE 5: ALTERNATIVE PATHS (Any stage can lead here)      │
    └────────────────────────────────────────────────────────────┘

    ┌──────────────────┐
    │   CANCELLED      │  ← Order cancelled
    │                  │  ← Before delivery: Ownership stays with supplier
    │ Status:CANCELLED │  ← After delivery: Cancellation details critical
    └──────────────────┘
```

---

## 👥 Ownership Transfer Process

```
                        OWNERSHIP JOURNEY
                        ═════════════════

Stage 1: PENDING
─────────────────────────────────────────────
  Lumber Yard:       Potential Buyer (awaiting delivery)
  Supplier:          Owner (responsible for shipment)
  Financial Risk:    On Supplier (until delivery)
  Insurance:         Supplier's responsibility
  
  Timeline:   Order created → Confirmed → In Transit → Delivery

            Status: Draft → Submitted → Confirmed → In Transit

                            │
                            │ DELIVERY OCCURS
                            ↓

Stage 2: TRANSFERRED
─────────────────────────────────────────────
  Lumber Yard:       Owner (took possession)
  Supplier:          No longer owner (responsibility transferred)
  Financial Risk:    ON LUMBER YARD (ownership changed)
  Insurance:         Now lumber yard's responsibility
  
  Timeline:   Goods delivered at site

            Status: Delivered
            actual_delivery_date: [recorded]
            delivery_notes: [documented]

                            │
                            │ INSPECTION
                            ↓

Stage 3: CONFIRMED
─────────────────────────────────────────────
  Lumber Yard:       Confirmed Owner (in inventory)
  Supplier:          Delivered (relationship complete)
  Financial Risk:    Fully on lumber yard
  Insurance:         Must be insured
  
  Timeline:   Inspection passed → Stocked in inventory

            Status: Stocked
            Ownership confirmed in RoundWoodInventory
            Available for sales/production


KEY POINTS:
───────────
✓ Stage 1 (PENDING):     Supplier responsible
✓ Stage 2 (TRANSFERRED): Ownership changes on delivery
✓ Stage 3 (CONFIRMED):   Confirmed in inventory
✓ Can't stock without inspection pass
✓ Clear audit trail of when ownership changed
✓ Complete cost tracking at each stage
```

---

## 📦 Data Model Relationships

```
┌─────────────────────────────────────────────────────────┐
│                    DATA RELATIONSHIPS                   │
└─────────────────────────────────────────────────────────┘

                       SUPPLIER
                          │
                          │
                          │ Has many
                          ↓
              ROUNDWOODPURCHASEORDER
                     (PO)
                          │
            ┌─────────────┼─────────────┐
            │             │             │
     References      Has many      Tracks
     WoodType        Items         Ownership
            │             │             │
            ↓             ↓             ↓
       Item 1          Item 2       Pending→
       Item 2          Item 3       Transferred→
       Item 3          Item N       Confirmed

                          │
                   (on stock-in)
                          ↓
              ROUNDWOODINVENTORY
                  (Current Stock)
                          │
                    Has many
                          ↓
           ROUNDWOODSTOCKTRANSACTION
                  (History)
                          │
                    Has many
                          ↓
             ROUNDWOODPROCUREMENTLOG
                   (Audit Trail)


DETAILED RELATIONSHIPS:
──────────────────────

Supplier (1) ─────Many─────> RoundWoodPurchaseOrder
                              - company_name
                              - contact info
                              - ratings

WoodType (1) ──────Many─────> RoundWoodPurchaseOrderItem
                              - species
                              - dimensions

RoundWoodPurchaseOrder (1) ──Many──> RoundWoodPurchaseOrderItem
                              - quantity_logs
                              - diameter_inches
                              - length_feet
                              - volume_cubic_feet
                              - subtotal

RoundWoodPurchaseOrderItem
              │
              │ (on stock-in)
              ↓
RoundWoodInventory (per WoodType)
              - total_logs_in_stock
              - total_cubic_feet_in_stock
              - total_cost_invested
              - average_cost_per_cubic_foot

RoundWoodInventory ──Many──> RoundWoodStockTransaction
                              - All log in/out movements
                              - Cost tracking
                              - Reference to PO

RoundWoodPurchaseOrder ──Many──> RoundWoodProcurementLog
                              - Every action logged
                              - Status changes
                              - Who made changes
                              - When changes made
```

---

## 💰 Cost Calculation Flow

```
┌────────────────────────────────────────────────────────────┐
│              COST CALCULATION PROCESS                     │
└────────────────────────────────────────────────────────────┘

STEP 1: VOLUME CALCULATION (Per Item)
────────────────────────────────────
   User Input:
   ┌─────────────────────┐
   │ Quantity: 100 logs  │
   │ Diameter: 12 inches │
   │ Length: 16 feet     │
   └─────────────────────┘
            │
            ↓
   Auto-Calculate:
   Volume = π × (D/2)² × L × Q / 12
   ┌────────────────────────────────┐
   │ π × (6)² × 16 × 100 / 12       │
   │ = 3.14159 × 36 × 16 × 100 / 12 │
   │ = ~500.00 cubic feet            │
   └────────────────────────────────┘


STEP 2: ITEM COST CALCULATION
──────────────────────────────
   Item Subtotal = Volume × Unit Cost
   ┌──────────────────────────────────┐
   │ 500 CF × ₱50/CF = ₱25,000        │
   └──────────────────────────────────┘


STEP 3: PO TOTAL CALCULATION
────────────────────────────
   PO Total = SUM(All Item Subtotals)
   
   Item 1: 500 CF × ₱50/CF = ₱25,000
   Item 2: 300 CF × ₱45/CF = ₱13,500
   Item 3: 200 CF × ₱48/CF = ₱9,600
   ───────────────────────────────────
   TOTAL:                    ₱48,100


STEP 4: INVENTORY VALUATION (After Stock-In)
─────────────────────────────────────────────
   Per Wood Type:
   
   Wood Type: Oak Logs
   ┌─────────────────────────────┐
   │ Quantity Accepted: 98 logs  │
   │ Volume (CF): 490.00         │
   │ Cost Invested: ₱24,500      │
   │ Avg Cost/CF: ₱50.00         │
   │ Warehouse: Yard A, Section B│
   └─────────────────────────────┘
   
   Calculation:
   Average Cost = Total Cost / Total Volume
                = ₱24,500 / 490 CF
                = ₱50.00 per CF


STEP 5: STOCK TRANSACTION RECORD
────────────────────────────────
   When stock-in completes, creates:
   
   RoundWoodStockTransaction
   ┌──────────────────────────────┐
   │ Type: Stock In               │
   │ Wood Type: Oak Logs          │
   │ Quantity: 98 logs            │
   │ Volume: 490.00 CF            │
   │ Cost/Unit: ₱50.00/CF         │
   │ Total Cost: ₱24,500          │
   │ Reference: RWPO-2024-001     │
   │ Created By: John Smith       │
   │ Timestamp: 2024-12-25 15:00  │
   └──────────────────────────────┘


FULL COST TRACE:
────────────────
Purchase Order ─→ Line Items (volumes calc'd)
                        ↓
                   Subtotals (per item)
                        ↓
                   PO Total (sum)
                        ↓
                   Stock-In (accepted qty only)
                        ↓
                   Inventory Record (valuation)
                        ↓
                   Stock Transaction (log)
                        ↓
            100% Cost Visibility & Audit Trail
```

---

## 🔍 Inspection Workflow

```
┌────────────────────────────────────────────────┐
│         INSPECTION WORKFLOW DETAIL             │
└────────────────────────────────────────────────┘

                    DELIVERY RECEIVED
                           │
                           ↓
              ┌──────────────────────────┐
              │  Create Inspection Task  │
              │  Status: PENDING         │
              │  Each PO gets assigned   │
              └──────────────────────────┘
                           │
                           ↓
              ┌──────────────────────────┐
              │  START INSPECTION        │
              │  Status: IN PROGRESS     │
              │  Inspector assigned      │
              │  Checklist prepared      │
              └──────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ↓                  ↓                  ↓

   PER-ITEM INSPECTION (Do for each batch)
   ──────────────────────────────────────
   
   Item 1: 100 logs (12" diameter, 16' length)
   ┌──────────────────────────────────┐
   │ Inspect all logs in batch        │
   │ Check:                           │
   │  - Diameter/length compliance    │
   │  - Visible defects (cracks)      │
   │  - Rot or damage                 │
   │  - Pest damage                   │
   │  - Moisture content              │
   │  - Species correctness           │
   ├──────────────────────────────────┤
   │ Result: 98 ACCEPTED, 2 REJECTED  │
   │                                  │
   │ Notes:                           │
   │ "2 logs with minor end cracks,   │
   │  within acceptable limits but    │
   │  classified as utility grade"    │
   └──────────────────────────────────┘
   
   Item 2: 80 logs (14" diameter, 16' length)
   ┌──────────────────────────────────┐
   │ Similar inspection process       │
   │ Result: 80 ACCEPTED, 0 REJECTED  │
   └──────────────────────────────────┘
   

   ┌──────────────────────────────────────┐
   │  COMPLETE INSPECTION                 │
   │  Status: PASSED (all items pass)     │
   │  Status: FAILED (any item fails)     │
   │  Status: PARTIAL (mix of pass/fail)  │
   ├──────────────────────────────────────┤
   │  Inspector: John Smith               │
   │  Timestamp: 2024-12-25 14:30:00      │
   │  Overall Notes: "All items meet      │
   │                 quality standards"   │
   └──────────────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
         ↓ PASSED              ↓ FAILED
    CAN STOCK-IN          CANNOT STOCK-IN
    Move to next          Return to PO for
    phase: Stock-In       review/correction
```

---

## 🗄️ Inventory Stock-In Process

```
┌────────────────────────────────────────────────┐
│    AUTOMATIC STOCK-IN PROCESS DIAGRAM          │
└────────────────────────────────────────────────┘

                INSPECTION PASSED
                        │
                        ↓
    ┌───────────────────────────────────────────┐
    │ Call: POST /api/round-wood-purchases/{id}/│
    │           stock_in/                       │
    └───────────────────────────────────────────┘
                        │
                        ↓
            ┌───────────────────────────┐
            │  TRIGGER STOCK-IN PROCESS │
            │  (Automatic Actions)      │
            └───────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ↓               ↓               ↓
    FOR EACH       CREATE/UPDATE      CREATE STOCK
    ACCEPTED       INVENTORY          TRANSACTION
    ITEM
        │               │               │
        │               ↓               ↓
        │        RoundWoodInventory
        │        ┌──────────────────┐  RoundWoodStock
        │        │ wood_type: Oak   │  Transaction
        │        │ logs: +98        │  ┌──────────────┐
        │        │ volume: +490 CF  │  │ type: stock_in
        │        │ cost: +₱24,500   │  │ reference: PO
        │        │ avg_cost: ₱50/CF │  │ cost: ₱24,500
        │        └──────────────────┘  └──────────────┘
        │
        ↓
    ┌────────────────────────────┐
    │  PO STATUS UPDATES         │
    │  status: INSPECTED → STOCKED│
    │  ownership: TRANSFERRED →   │
    │             CONFIRMED       │
    │  is_fully_stocked: true     │
    │  timestamp: [now]           │
    └────────────────────────────┘
                │
                ↓
    ┌────────────────────────────┐
    │  CREATE PROCUREMENT LOG    │
    │  action: "stocked"         │
    │  details: "98 items...     │
    │           successfully     │
    │           stocked"         │
    │  performed_by: User        │
    │  timestamp: [now]          │
    └────────────────────────────┘
                │
                ↓
        ✅ COMPLETE ✅
        
    Stock added to inventory
    Ownership confirmed
    Ready for sales/production
    Complete audit trail created
```

---

## 📊 Status Transition Matrix

```
FROM\TO        Draft  Submit Confirm Transit Deliver Inspect Stocked Cancel
──────────────────────────────────────────────────────────────────────────
Draft           -      ✓      -      -      -       -        -       ✓
Submitted       -      -      ✓      -      -       -        -       ✓
Confirmed       -      -      -      ✓      -       -        -       ✓
In Transit      -      -      -      -      ✓       -        -       ✓
Delivered       -      -      -      -      -       ✓        -       ✓
Inspected       -      -      -      -      -       -        ✓       ✓
Stocked         -      -      -      -      -       -        -       ✗
Cancelled       -      -      -      -      -       -        -       -

Legend: ✓ = Valid transition  ✗ = Invalid transition  - = N/A
```

---

## 🏪 Dashboard Widget Ideas

```
┌────────────────────────────────────────────────────────┐
│          ROUND WOOD PURCHASING WIDGETS                │
├────────────────────────────────────────────────────────┤
│                                                        │
│ ┌──────────────────────┐  ┌──────────────────────┐   │
│ │ Pending Orders       │  │ Inventory Value      │   │
│ │ Count: 5             │  │ ₱450,000             │   │
│ │ Volume: 2500 CF      │  │ 1200 logs            │   │
│ └──────────────────────┘  └──────────────────────┘   │
│                                                        │
│ ┌──────────────────────┐  ┌──────────────────────┐   │
│ │ Pending Inspection   │  │ Total Stocked YTD    │   │
│ │ Count: 2             │  │ 50 orders            │   │
│ │ Volume: 800 CF       │  │ ₱2,500,000           │   │
│ └──────────────────────┘  └──────────────────────┘   │
│                                                        │
│ ┌────────────────────────────────────────────────┐   │
│ │ Recent Orders                                  │   │
│ │ ─────────────────────────────────────────────  │   │
│ │ RWPO-2024-001  Oak Logs      500 CF  STOCKED   │   │
│ │ RWPO-2024-002  Pine Logs     300 CF  INSPECTING│   │
│ │ RWPO-2024-003  Teak Logs     200 CF  DELIVERED │   │
│ └────────────────────────────────────────────────┘   │
│                                                        │
│ ┌────────────────────────────────────────────────┐   │
│ │ Cost Trend (Last 90 Days)                      │   │
│ │ [Line chart showing cost by week]              │   │
│ └────────────────────────────────────────────────┘   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 🔄 Integration Points Map

```
                    ROUND WOOD PURCHASING
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ↓                     ↓                     ↓
    
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ INVENTORY    │  │ SUPPLIER     │  │ REPORTING    │
    │ MODULE       │  │ MODULE       │  │ MODULE       │
    ├──────────────┤  ├──────────────┤  ├──────────────┤
    │ • Stock-in   │  │ • Link to    │  │ • Purchase   │
    │ • Track qty  │  │   supplier   │  │   summary    │
    │ • Value      │  │ • Track PO   │  │ • Cost       │
    │   tracking   │  │   numbers    │  │   analysis   │
    │ • Audit trail│  │ • Performance│  │ • Supplier   │
    │              │  │   metrics    │  │   metrics    │
    └──────────────┘  └──────────────┘  └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   WOOD LOGS       │
                    │   IN INVENTORY    │
                    │   Ready for:      │
                    │   - Sales         │
                    │   - Production    │
                    │   - Processing    │
                    └───────────────────┘
```

---

## 📱 API Call Flow

```
┌───────────────────────────────────────────────┐
│          TYPICAL API CALL SEQUENCE            │
└───────────────────────────────────────────────┘

1. CREATE PURCHASE ORDER
   POST /api/round-wood-purchases/
   {po_number, supplier, expected_delivery, unit_cost}
   ↓ Returns: PO object with status="draft"

2. ADD ITEMS
   POST /api/round-wood-items/
   {purchase_order, wood_type, quantity_logs, diameter, length, cost}
   ↓ Returns: Item object with auto-calculated volume & subtotal

3. SUBMIT
   POST /api/round-wood-purchases/1/submit/
   ↓ Returns: PO with status="submitted"

4. CONFIRM
   POST /api/round-wood-purchases/1/confirm/
   ↓ Returns: PO with status="confirmed", approved_by set

5. MARK DELIVERED
   POST /api/round-wood-purchases/1/mark_delivered/
   {delivery_date, delivery_notes}
   ↓ Returns: PO with status="delivered", ownership="transferred"

6. START INSPECTION
   POST /api/round-wood-purchases/1/start_inspection/
   ↓ Returns: PO with inspection_status="in_progress"

7. INSPECT ITEMS
   POST /api/round-wood-items/1/inspect_item/
   {status, quantity_accepted, notes}
   ↓ Returns: Item with inspection_status updated

8. COMPLETE INSPECTION
   POST /api/round-wood-purchases/1/complete_inspection/
   {inspector_name, inspection_notes, result}
   ↓ Returns: PO with inspection_status="passed"

9. STOCK IN
   POST /api/round-wood-purchases/1/stock_in/
   ↓ Returns: Success message
   ↓ Automatically creates:
   │  - RoundWoodInventory
   │  - RoundWoodStockTransaction
   │  - RoundWoodProcurementLog
   ↓ Sets: status="stocked", ownership="confirmed"

10. VIEW RESULTS
    GET /api/round-wood-inventory/
    ↓ Shows updated stock levels
    GET /api/round-wood-transactions/
    ↓ Shows all movements
    GET /api/round-wood-logs/
    ↓ Shows complete audit trail
    GET /api/round-wood-purchases/summary/
    ↓ Shows statistics
```

---

**End of Visual Guide**

For detailed explanations, see the main implementation guide.

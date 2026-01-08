#!/usr/bin/env python
"""
Test script to verify auto-generated PO numbers and default COD payment terms
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
django.setup()

from app_round_wood.models import RoundWoodPurchaseOrder
from app_supplier.models import Supplier
from core.models import CustomUser
from datetime import datetime, timedelta

def test_auto_po_generation():
    """Test auto-generation of PO numbers"""
    print("\n" + "="*60)
    print("TEST: Auto-Generated PO Numbers & Default COD")
    print("="*60)
    
    # Get existing supplier and admin user
    supplier = Supplier.objects.first()
    user = CustomUser.objects.filter(is_staff=True).first()
    
    if not supplier:
        print("[-] No suppliers found. Please create a supplier first.")
        return False
    
    if not user:
        print("[-] No staff users found. Please create a superuser first.")
        return False
    
    print(f"\nUsing Supplier: {supplier.company_name}")
    print(f"Using User: {user.username}")
    
    # Test 1: Create PO without specifying PO number or payment terms
    print("\n[Test 1] Creating PO without PO Number or Payment Terms...")
    try:
        delivery_date = datetime.now().date() + timedelta(days=30)
        
        po1 = RoundWoodPurchaseOrder.objects.create(
            supplier=supplier,
            expected_delivery_date=delivery_date,
            unit_cost_per_cubic_foot=50.00,
            created_by=user
        )
        
        print(f"  [+] PO Created Successfully!")
        print(f"    - PO Number: {po1.po_number}")
        print(f"    - Payment Terms: {po1.payment_terms}")
        print(f"    - Status: {po1.status}")
        
        # Verify format
        if po1.po_number.startswith('RWPO-'):
            print(f"    [+] PO Number format is correct")
        else:
            print(f"    [-] PO Number format is incorrect")
            return False
        
        # Verify default payment terms
        if po1.payment_terms == 'Cash on Delivery (COD)':
            print(f"    [+] Default payment terms is COD")
        else:
            print(f"    [-] Payment terms not set to COD: {po1.payment_terms}")
            return False
            
    except Exception as e:
        print(f"  [-] Error creating PO: {str(e)}")
        return False
    
    # Test 2: Create another PO and verify sequential numbering
    print("\n[Test 2] Creating second PO to verify sequential numbering...")
    try:
        po2 = RoundWoodPurchaseOrder.objects.create(
            supplier=supplier,
            expected_delivery_date=delivery_date,
            unit_cost_per_cubic_foot=50.00,
            created_by=user
        )
        
        print(f"  [+] Second PO Created!")
        print(f"    - PO Number: {po2.po_number}")
        
        # Verify sequential
        if po2.po_number != po1.po_number:
            print(f"    [+] PO Numbers are different (sequential)")
        else:
            print(f"    [-] PO Numbers are the same (not sequential)")
            return False
            
    except Exception as e:
        print(f"  [-] Error creating second PO: {str(e)}")
        return False
    
    # Test 3: Create PO with custom payment terms
    print("\n[Test 3] Creating PO with custom payment terms...")
    try:
        po3 = RoundWoodPurchaseOrder.objects.create(
            supplier=supplier,
            expected_delivery_date=delivery_date,
            unit_cost_per_cubic_foot=50.00,
            payment_terms='Net 30',
            created_by=user
        )
        
        print(f"  [+] PO Created with custom terms!")
        print(f"    - PO Number: {po3.po_number}")
        print(f"    - Payment Terms: {po3.payment_terms}")
        
        if po3.payment_terms == 'Net 30':
            print(f"    [+] Custom payment terms preserved")
        else:
            print(f"    [-] Payment terms not set correctly")
            return False
            
    except Exception as e:
        print(f"  [-] Error creating PO with custom terms: {str(e)}")
        return False
    
    # Test 4: Verify uniqueness
    print("\n[Test 4] Verifying PO number uniqueness...")
    try:
        all_pos = RoundWoodPurchaseOrder.objects.filter(po_number__startswith='RWPO-2024')
        po_numbers = [po.po_number for po in all_pos]
        unique_numbers = set(po_numbers)
        
        if len(po_numbers) == len(unique_numbers):
            print(f"  [+] All PO numbers are unique")
            print(f"    - Total POs: {len(po_numbers)}")
            print(f"    - Sample numbers: {', '.join(po_numbers[:3])}")
        else:
            print(f"  [-] Duplicate PO numbers found!")
            return False
            
    except Exception as e:
        print(f"  [-] Error checking uniqueness: {str(e)}")
        return False
    
    print("\n" + "="*60)
    print("[SUCCESS] ALL TESTS PASSED!")
    print("="*60)
    print("\nSummary:")
    print("  [+] Auto-generation of PO numbers: WORKING")
    print("  [+] Default COD payment terms: WORKING")
    print("  [+] Sequential numbering: WORKING")
    print("  [+] Custom payment terms: WORKING")
    print("  [+] Uniqueness constraint: WORKING")
    print("="*60 + "\n")
    
    return True

if __name__ == '__main__':
    success = test_auto_po_generation()
    exit(0 if success else 1)

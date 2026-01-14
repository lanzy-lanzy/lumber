import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings') 
django.setup()

from django.core.cache import cache
from app_inventory.models import LumberProduct, StockTransaction
from app_inventory.services import InventoryService

def test_cache_invalidation():
    print("Testing cache invalidation...")
    
    # Setup
    product = LumberProduct.objects.filter(is_active=True).first()
    if not product:
        print("No active products found to test with.")
        return

    print(f"Testing with product: {product.name} (ID: {product.id})")
    
    # 1. Initial State
    initial_inventory = product.inventory.quantity_pieces
    print(f"Initial Inventory: {initial_inventory}")
    
    # 2. Access Product List API to trigger caching
    # This simulates a user viewing the product list
    # We need to manually access the cache or simulate a request
    cache_key = f"product_{product.id}"
    cache.set(cache_key, {"dummy": "data"}, 300) # Manually set a cache to see if logic clears it
    
    print(f"Cache key '{cache_key}' set explicitly.")
    
    # 3. Perform Stock Out
    print("Performing Stock Out of 1 piece...")
    try:
        InventoryService.stock_out(
            product_id=product.id,
            quantity_pieces=1,
            reason="Test Verification",
            created_by=None,
            reference_id=""
        )
    except Exception as e:
        print(f"Stock out failed: {e}")
        return

    # 4. Verify Cache is Cleared
    cached_val = cache.get(cache_key)
    if cached_val is None:
        print("SUCCESS: Product cache was invalidated.")
    else:
        print("FAILURE: Product cache still exists.")

    # 5. Verify Version Increment (List Cache)
    # We can check if the version key was incremented or set
    version = cache.get('products_list_version')
    print(f"Current products_list_version: {version}")
    
    # Cleanup (restore inventory)
    print("Restoring inventory...")
    InventoryService.adjust_stock(
        product_id=product.id,
        quantity_change=1,
        reason="Test Cleanup",
        created_by=None
    )
    print("Test complete.")

if __name__ == "__main__":
    try:
        test_cache_invalidation()
    except Exception as e:
        print(f"An error occurred: {e}")

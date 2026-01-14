from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from app_inventory.models import Inventory, StockTransaction, LumberProduct

@receiver([post_save, post_delete], sender=Inventory)
@receiver([post_save, post_delete], sender=StockTransaction)
@receiver([post_save, post_delete], sender=LumberProduct)
def invalid_product_cache(sender, instance, **kwargs):
    """
    Invalidate product cache when inventory changes.
    This ensures that the product list reflects the latest stock levels immediately.
    """
    # 1. Clear specific product cache if possible
    product_id = None
    if isinstance(instance, LumberProduct):
        product_id = instance.id
    elif isinstance(instance, Inventory):
        product_id = instance.product_id
    elif isinstance(instance, StockTransaction):
        product_id = instance.product_id
        
    if product_id:
        # Clear individual product detail cache
        cache.delete(f"product_{product_id}")
    
    # 2. Clear product list caches
    # Since we can't accept wildcard deletions on all cache backends reliably,
    # we use the versioning strategy pattern from the ViewSet.
    
    # Increment the version to invalidate all list caches
    try:
        if hasattr(cache, 'incr'):
            try:
                cache.incr('products_list_version')
            except ValueError:
                # If key doesn't exist yet
                cache.set('products_list_version', 2)
        else:
            # Fallback for backends without atomic incr
            v = cache.get('products_list_version', 1)
            cache.set('products_list_version', int(v) + 1)
            
    except Exception as e:
        print(f"Error invalidating product cache: {e}")
        # Last resort: try to delete pattern if supported (Redis)
        if hasattr(cache, 'delete_pattern'):
            try:
                cache.delete_pattern("products_list_*")
            except Exception:
                pass

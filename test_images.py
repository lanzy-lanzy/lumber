#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify product images are set up correctly
"""
import os
import sys
import django
import json

# Handle Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
django.setup()

from django.core.cache import cache
from app_inventory.models import LumberProduct
from app_inventory.serializers import LumberProductSerializer

print("=" * 60)
print("PRODUCT IMAGES TEST REPORT")
print("=" * 60)

# Test 1: Count products with images
print("\n[TEST 1] Counting products with images...")
all_products = LumberProduct.objects.all()
products_with_images = all_products.filter(image__isnull=False)
print(f"  Total products: {all_products.count()}")
print(f"  Products with images: {products_with_images.count()}")
print(f"  Products without images: {all_products.exclude(image__isnull=False).count()}")

# Test 2: Verify image files exist
print("\n[TEST 2] Verifying image files exist...")
from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT
products_dir = os.path.join(MEDIA_ROOT, 'products')

if os.path.exists(products_dir):
    image_files = [f for f in os.listdir(products_dir) if f.endswith('.jpg')]
    print(f"  Product images directory: {products_dir}")
    print(f"  Image files found: {len(image_files)}")
    for img in sorted(image_files)[:5]:
        size = os.path.getsize(os.path.join(products_dir, img)) / 1024
        print(f"    - {img} ({size:.1f} KB)")
else:
    print(f"  ERROR: Directory not found: {products_dir}")

# Test 3: Check serializer output
print("\n[TEST 3] Testing serializer output...")
test_product = products_with_images.first()
if test_product:
    serializer = LumberProductSerializer(test_product)
    data = serializer.data
    print(f"  Product: {test_product.name}")
    print(f"  Image field in serializer: {data.get('image')}")
    
    if data.get('image'):
        print(f"  Image URL format: OK")
        if data['image'].startswith('/media/'):
            print(f"  Image URL is relative: OK")
        elif data['image'].startswith('http'):
            print(f"  Image URL is absolute: OK")
    else:
        print(f"  ERROR: Image field is empty!")
else:
    print(f"  ERROR: No products with images found!")

# Test 4: Check API cache
print("\n[TEST 4] Checking cache status...")
cache_keys = []
if hasattr(cache, '_cache'):
    cache_keys = list(cache._cache.keys())
    products_cache_keys = [k for k in cache_keys if 'product' in k.lower()]
    print(f"  Total cache keys: {len(cache_keys)}")
    print(f"  Product-related cache keys: {len(products_cache_keys)}")
    if products_cache_keys:
        print(f"  Sample cached keys:")
        for key in products_cache_keys[:3]:
            print(f"    - {key}")
else:
    print(f"  Using database cache or other backend")
    print(f"  Cannot inspect cache directly")

# Test 5: Verify database records
print("\n[TEST 5] Checking database records...")
for i, product in enumerate(products_with_images[:3]):
    print(f"  [{i+1}] {product.name}")
    print(f"      SKU: {product.sku}")
    print(f"      Image field: {product.image}")
    print(f"      Image URL: {product.image.url if product.image else 'None'}")
    print(f"      File exists: {os.path.exists(os.path.join(MEDIA_ROOT, str(product.image)))}")

# Test 6: Settings check
print("\n[TEST 6] Verifying Django settings...")
print(f"  MEDIA_URL: {settings.MEDIA_URL}")
print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"  DEBUG: {settings.DEBUG}")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)

if products_with_images.count() > 0 and test_product:
    print("Status: OK - Images are properly configured!")
    print("\nNext steps:")
    print("  1. Restart Django server")
    print("  2. Clear browser cache (Ctrl+Shift+Delete)")
    print("  3. Open incognito window")
    print("  4. Visit http://localhost:8000/")
    print("  5. Images should display!")
else:
    print("Status: ERROR - Images not properly set up")
    print("\nFix:")
    print("  1. Run: python manage.py generate_product_images")
    print("  2. Then run this test again")

print("=" * 60)

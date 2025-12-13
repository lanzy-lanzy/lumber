#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

# Handle Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
django.setup()

from django.core.cache import cache
cache.clear()
print("[OK] Cache cleared successfully!")

# Also verify products have images
from app_inventory.models import LumberProduct
products_with_images = LumberProduct.objects.filter(image__isnull=False)
print(f"[OK] {products_with_images.count()} products have images")

for product in products_with_images:
    print(f"  - {product.name}: {product.image.url}")

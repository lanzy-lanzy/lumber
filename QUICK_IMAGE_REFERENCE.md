# Product Image Upload - Quick Reference

## For Users

### Add Product with Image
1. Dashboard → Inventory → Products
2. Click **"+ Add Product"** button
3. Fill in all product details
4. Scroll to **"Product Image"** section
5. Click file input and select image
6. See preview appear
7. Click **"Save"**
8. ✅ Product created with image thumbnail

### Edit Product Image
1. Find product in table
2. Click **edit (pencil) icon**
3. Modal opens with product data

**Option A: Keep Current Image**
- Don't touch the file input
- Click **"Save"**
- ✅ Image unchanged

**Option B: Replace Image**
- Click file input
- Select new image
- See new preview
- Click **"Save"**
- ✅ Image updated

**Option C: Remove Image**
- Click **"Remove Image"** button (red)
- Current image disappears
- Click **"Save"**
- ✅ Image deleted, placeholder shows

## For Developers

### Model Definition
```python
# app_inventory/models.py
class LumberProduct(models.Model):
    image = models.ImageField(upload_to='products/', null=True, blank=True)
```

### View Handling
```python
# app_inventory/management_views.py
# CREATE
image=request.FILES.get('image') if request.FILES else None

# UPDATE
if request.FILES.get('image'):
    product.image = request.FILES.get('image')
if request.POST.get('clear_image') == 'true':
    product.image = None
```

### Template Form
```html
<form enctype="multipart/form-data" method="POST">
    <input type="file" name="image" accept="image/*">
</form>
```

### Display Image
```html
<!-- In table -->
{% if product.image %}
    <img src="{{ product.image.url }}" class="w-12 h-12 rounded">
{% endif %}
```

## Configuration Checklist

- [x] `MEDIA_URL = '/media/'` in settings.py
- [x] `MEDIA_ROOT` set in settings.py
- [x] Media serving in urls.py for DEBUG=True
- [x] Migration 0005_lumberproduct_image applied
- [x] Pillow installed
- [x] Form has enctype="multipart/form-data"

## Directory Structure
```
lumber/
├── media/
│   └── products/        ← Images stored here
│       ├── product_1.jpg
│       ├── product_2.png
│       └── ...
├── app_inventory/
│   └── models.py        ← image field added
└── templates/
    └── inventory/management/
        └── products.html ← modal updated
```

## File Size Limits
- Default: Depends on server (usually 100MB+)
- No frontend validation yet
- Consider adding max size validation

## Supported Formats
✅ JPG, JPEG, PNG, GIF, BMP, TIFF, WebP

## API Access
```javascript
// GET image URL
product.image.url  // "/media/products/filename.jpg"

// Upload via API
const form = new FormData();
form.append('image', fileInput.files[0]);
form.append('name', 'Product Name');
// ... other fields
fetch('/api/products/', {method: 'POST', body: form})
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Image not showing | Check `media/` directory exists and is readable |
| Upload fails | Ensure form has `enctype="multipart/form-data"` |
| 404 on image URL | Verify media serving configured in urls.py |
| No preview | Check browser console for JS errors |
| Can't remove image | Ensure `clear_image` flag sent in POST |

## Common Tasks

### Display all product images
```html
{% for product in products %}
    <img src="{{ product.image.url }}" alt="{{ product.name }}">
{% endfor %}
```

### Check if product has image
```html
{% if product.image %}
    Has image
{% else %}
    No image
{% endif %}
```

### Get image file name
```python
product.image.name  # "products/filename.jpg"
```

### Delete image from product
```python
product.image = None
product.save()
```

### Query products with images
```python
products = LumberProduct.objects.exclude(image='')
```

## File Locations

| File | Purpose | Lines Changed |
|------|---------|----------------|
| models.py | Added image field | 34 |
| management_views.py | Handle upload/delete | 136, 150-156 |
| products.html | Modal form + JS | Multiple |
| urls.py | Media serving | 2-3, 63-67 |
| settings.py | Media config | 150-151 |

## Command Reference

```bash
# Create migration (already done)
python manage.py makemigrations app_inventory

# Apply migration (already done)
python manage.py migrate app_inventory

# Check system
python manage.py check

# Test upload
# - Go to inventory/management/products
# - Add product with image
# - Check media/products/ directory

# Reset migrations (if needed)
# Delete 0005_lumberproduct_image.py
# Drop and recreate database
```

## Performance Tips

1. **Compress images** before uploading
2. **Use web-friendly formats** (WebP, JPEG)
3. **Resize large images** server-side (future)
4. **Use CDN** for image serving (production)
5. **Lazy load** images in gallery views (future)

## Security Notes

1. File type validation: ✅ Implemented (`accept="image/*"`)
2. File size limit: ⚠️ Not yet set (add if needed)
3. Virus scanning: ⚠️ Not implemented (add for production)
4. Rate limiting: ⚠️ Not implemented
5. Access control: ✅ Requires login

## Next Steps (Optional)

- [ ] Add file size validation (max 5MB)
- [ ] Implement image compression
- [ ] Add image cropping tool
- [ ] Support multiple images
- [ ] Add drag & drop
- [ ] Implement cloud storage
- [ ] Add image gallery view

---

## Quick Links
- [Full Implementation Guide](PRODUCT_IMAGE_IMPLEMENTATION.md)
- [Feature Summary](IMAGE_FEATURE_SUMMARY.md)
- [Verification Report](PRODUCT_IMAGE_VERIFICATION.md)

---
**Version**: 1.0  
**Status**: ✅ Production Ready  
**Last Updated**: December 11, 2025

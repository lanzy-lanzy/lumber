from rest_framework import serializers
from app_inventory.models import LumberCategory, LumberProduct, Inventory, StockTransaction


class LumberCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LumberCategory
        fields = ['id', 'name', 'description', 'created_at']


class InventoryQuickSerializer(serializers.ModelSerializer):
    """Quick inventory serializer for nested in product"""
    class Meta:
        model = Inventory
        fields = ['quantity_pieces', 'total_board_feet']


class LumberProductSerializer(serializers.ModelSerializer):
    board_feet = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()
    # Readable URL for image
    image = serializers.SerializerMethodField()
    # Writable image field (for uploads/replacements)
    image_file = serializers.ImageField(write_only=True, required=False, allow_null=True)
    # Flag to remove existing image
    remove_image = serializers.BooleanField(write_only=True, required=False, default=False)
    
    class Meta:
        model = LumberProduct
        fields = ['id', 'name', 'category', 'thickness', 'width', 'length', 'board_feet', 
                  'price_per_board_foot', 'price_per_piece', 'sku', 'is_active', 'inventory', 'image', 'image_file', 'remove_image', 'created_at', 'updated_at']
    
    def get_board_feet(self, obj):
        return float(obj.board_feet)
    
    def get_inventory(self, obj):
        try:
            inventory = obj.inventory
            return {
                'quantity_pieces': inventory.quantity_pieces,
                'total_board_feet': float(inventory.total_board_feet)
            }
        except Inventory.DoesNotExist:
            return {
                'quantity_pieces': 0,
                'total_board_feet': 0.0
            }
    
    def get_image(self, obj):
        """Return full URL for image or None if no image"""
        if obj.image:
            try:
                # Try to get absolute URL from request context
                request = self.context.get('request')
                if request:
                    # Append a version query param based on updated_at to bust browser cache
                    try:
                        ver = int(obj.updated_at.timestamp()) if getattr(obj, 'updated_at', None) else None
                    except Exception:
                        ver = None
                    url = obj.image.url
                    if ver:
                        sep = '&' if '?' in url else '?'
                        url = f"{url}{sep}v={ver}"
                    return request.build_absolute_uri(url)
            except Exception as e:
                print(f"Error building absolute URI: {e}")
            
            # Fallback: return relative URL (works in development)
            image_url = obj.image.url
            # Ensure it starts with / for relative URL
            if not image_url.startswith('/'):
                image_url = '/' + image_url
            # Append version param to bust browser cache
            try:
                ver = int(obj.updated_at.timestamp()) if getattr(obj, 'updated_at', None) else None
            except Exception:
                ver = None
            if ver:
                sep = '&' if '?' in image_url else '?'
                image_url = f"{image_url}{sep}v={ver}"
            return image_url
        return None

    def create(self, validated_data):
        image_file = validated_data.pop('image_file', None)
        # Accept file sent as 'image' in request.FILES (frontend compatibility)
        request = self.context.get('request')
        if not image_file and request is not None:
            image_file = request.FILES.get('image')
        # remove_image ignored on create
        product = super().create(validated_data)
        if image_file:
            product.image = image_file
            product.save()
        return product

    def update(self, instance, validated_data):
        # Handle image replacement or removal
        remove_image = validated_data.pop('remove_image', False)
        image_file = validated_data.pop('image_file', None)
        # Accept file sent as 'image' in request.FILES (frontend compatibility)
        request = self.context.get('request')
        if not image_file and request is not None:
            image_file = request.FILES.get('image')

        instance = super().update(instance, validated_data)

        if remove_image:
            # Clear existing image
            instance.image.delete(save=False)
            instance.image = None
            instance.save()
        elif image_file:
            # Replace existing image
            # Delete old file to avoid orphaned files
            try:
                instance.image.delete(save=False)
            except Exception:
                pass
            instance.image = image_file
            instance.save()

        return instance


class InventorySerializer(serializers.ModelSerializer):
    product = LumberProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_id', 'quantity_pieces', 'total_board_feet', 'last_updated']


class StockTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockTransaction
        fields = ['id', 'product', 'product_name', 'transaction_type', 'quantity_pieces', 'board_feet',
                  'reason', 'reference_id', 'cost_per_unit', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

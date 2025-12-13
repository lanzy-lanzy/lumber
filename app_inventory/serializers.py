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
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = LumberProduct
        fields = ['id', 'name', 'category', 'thickness', 'width', 'length', 'board_feet', 
                  'price_per_board_foot', 'price_per_piece', 'sku', 'is_active', 'inventory', 'image', 'created_at', 'updated_at']
    
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
                    return request.build_absolute_uri(obj.image.url)
            except Exception as e:
                print(f"Error building absolute URI: {e}")
            
            # Fallback: return relative URL (works in development)
            image_url = obj.image.url
            # Ensure it starts with / for relative URL
            if not image_url.startswith('/'):
                image_url = '/' + image_url
            return image_url
        return None


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

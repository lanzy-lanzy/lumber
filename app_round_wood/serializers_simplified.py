from rest_framework import serializers
from .models import WoodType, RoundWoodPurchaseOrder, RoundWoodPurchaseOrderItem, RoundWoodInventory


class WoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WoodType
        fields = [
            'id', 'name', 'species', 'description',
            'default_diameter_inches', 'default_length_feet',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class RoundWoodPurchaseOrderItemSerializer(serializers.ModelSerializer):
    wood_type_name = serializers.CharField(source='wood_type.name', read_only=True)
    
    class Meta:
        model = RoundWoodPurchaseOrderItem
        fields = [
            'id', 'purchase_order', 'wood_type', 'wood_type_name',
            'quantity_logs', 'diameter_inches', 'length_feet',
            'volume_cubic_feet', 'unit_cost_per_cubic_foot',
            'subtotal', 'created_at', 'updated_at'
        ]
        read_only_fields = ['subtotal', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Calculate volume and subtotal"""
        if 'volume_cubic_feet' not in data or data['volume_cubic_feet'] == 0:
            # Auto-calculate from diameter, length, quantity
            import math
            diameter_inches = data.get('diameter_inches')
            length_feet = data.get('length_feet')
            quantity_logs = data.get('quantity_logs')
            
            if diameter_inches and length_feet and quantity_logs:
                diameter_feet = diameter_inches / 12
                radius_feet = diameter_feet / 2
                volume_per_log = math.pi * (radius_feet ** 2) * float(length_feet)
                data['volume_cubic_feet'] = volume_per_log * quantity_logs
        
        return data


class RoundWoodPurchaseOrderListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list view"""
    supplier_name = serializers.CharField(source='supplier.company_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = RoundWoodPurchaseOrder
        fields = [
            'id', 'po_number', 'supplier', 'supplier_name',
            'status', 'payment_status', 'order_date', 'delivery_date',
            'total_volume_cubic_feet', 'total_amount',
            'created_by_name', 'created_at'
        ]
        read_only_fields = ['po_number', 'created_at']


class RoundWoodPurchaseOrderDetailSerializer(serializers.ModelSerializer):
    """Full serializer with nested items"""
    items = RoundWoodPurchaseOrderItemSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.company_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = RoundWoodPurchaseOrder
        fields = [
            'id', 'po_number', 'po_number_supplier',
            'supplier', 'supplier_name',
            'status', 'payment_status',
            'order_date', 'delivery_date',
            'total_volume_cubic_feet', 'unit_cost_per_cubic_foot',
            'total_amount', 'notes',
            'items', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['po_number', 'total_amount', 'created_at', 'updated_at']
    
    def update(self, instance, validated_data):
        """Prevent updating certain fields once delivered"""
        if instance.status == 'delivered':
            # Can't change supplier, amounts once delivered
            validated_data.pop('supplier', None)
            validated_data.pop('unit_cost_per_cubic_foot', None)
        
        return super().update(instance, validated_data)


class RoundWoodPurchaseOrderSimpleSerializer(serializers.ModelSerializer):
    """Minimal serializer for creation"""
    class Meta:
        model = RoundWoodPurchaseOrder
        fields = [
            'supplier', 'unit_cost_per_cubic_foot',
            'order_date', 'notes'
        ]


class RoundWoodInventorySerializer(serializers.ModelSerializer):
    wood_type_name = serializers.CharField(source='wood_type.name', read_only=True)
    
    class Meta:
        model = RoundWoodInventory
        fields = [
            'id', 'wood_type', 'wood_type_name',
            'total_logs_in_stock', 'total_cubic_feet_in_stock',
            'total_cost_invested', 'average_cost_per_cubic_foot',
            'warehouse_location', 'last_stock_in_date', 'last_updated'
        ]
        read_only_fields = [
            'total_logs_in_stock', 'total_cubic_feet_in_stock',
            'total_cost_invested', 'average_cost_per_cubic_foot',
            'last_stock_in_date', 'last_updated'
        ]

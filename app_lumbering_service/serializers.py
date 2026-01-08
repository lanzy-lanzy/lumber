from rest_framework import serializers
from .models import (
    LumberingServiceOrder,
    LumberingServiceOutput,
    ShavingsRecord
)
from app_sales.models import Customer


class LumberingServiceOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumberingServiceOutput
        fields = [
            'id',
            'service_order',
            'lumber_type',
            'quantity_pieces',
            'length_feet',
            'width_inches',
            'thickness_inches',
            'board_feet',
            'grade',
            'notes',
            'recorded_at',
            'updated_at'
        ]
        read_only_fields = ['board_feet', 'recorded_at', 'updated_at']


class ShavingsRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShavingsRecord
        fields = [
            'id',
            'service_order',
            'quantity',
            'unit',
            'customer_share',
            'company_share',
            'notes',
            'recorded_at',
            'updated_at'
        ]
        read_only_fields = ['recorded_at', 'updated_at']


class LumberingServiceOrderSerializer(serializers.ModelSerializer):
    outputs = LumberingServiceOutputSerializer(many=True, read_only=True)
    shavings = ShavingsRecordSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    actual_output_bf = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = LumberingServiceOrder
        fields = [
            'id',
            'customer',
            'customer_name',
            'received_date',
            'completed_date',
            'status',
            'wood_type',
            'quantity_logs',
            'estimated_board_feet',
            'service_fee_per_bf',
            'total_service_fee',
            'shavings_ownership',
            'actual_output_bf',
            'outputs',
            'shavings',
            'notes',
            'created_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['total_service_fee', 'actual_output_bf', 'created_at', 'updated_at']

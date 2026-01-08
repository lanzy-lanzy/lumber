from django.contrib import admin
from .models import (
    WoodType,
    RoundWoodPurchase,
    RoundWoodInventory
)


@admin.register(WoodType)
class WoodTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'is_active']
    list_filter = ['species', 'is_active']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'species', 'description', 'is_active')
        }),
        ('Default Measurements', {
            'fields': ('default_diameter_inches', 'default_length_feet')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RoundWoodPurchase)
class RoundWoodPurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'wood_type', 'quantity_logs', 'volume_cubic_feet',
                    'total_cost', 'status', 'purchase_date']
    list_filter = ['status', 'supplier', 'wood_type', 'purchase_date']
    search_fields = ['supplier__company_name', 'wood_type__name', 'notes']
    readonly_fields = ['volume_cubic_feet', 'total_cost', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Supplier Information', {
            'fields': ('supplier',)
        }),
        ('Wood Details', {
            'fields': ('wood_type', 'quantity_logs', 'diameter_inches', 'length_feet')
        }),
        ('Volume & Cost', {
            'fields': ('volume_cubic_feet', 'unit_cost_per_cubic_foot', 'total_cost')
        }),
        ('Purchase Information', {
            'fields': ('purchase_date', 'status')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Audit Trail', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RoundWoodInventory)
class RoundWoodInventoryAdmin(admin.ModelAdmin):
    list_display = ['wood_type', 'total_logs_in_stock', 'total_cubic_feet_in_stock',
                    'average_cost_per_cubic_foot', 'warehouse_location']
    list_filter = ['wood_type', 'last_stock_in_date']
    search_fields = ['wood_type__name', 'warehouse_location']
    readonly_fields = ['total_logs_in_stock', 'total_cubic_feet_in_stock',
                       'total_cost_invested', 'average_cost_per_cubic_foot',
                       'last_stock_in_date', 'last_updated']
    
    fieldsets = (
        ('Wood Type', {
            'fields': ('wood_type',)
        }),
        ('Stock Information', {
            'fields': ('total_logs_in_stock', 'total_cubic_feet_in_stock', 'warehouse_location')
        }),
        ('Cost Tracking', {
            'fields': ('total_cost_invested', 'average_cost_per_cubic_foot')
        }),
        ('Timestamps', {
            'fields': ('last_stock_in_date', 'last_updated'),
            'classes': ('collapse',)
        }),
    )

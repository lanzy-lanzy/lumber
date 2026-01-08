from django.contrib import admin
from django.utils.html import format_html
from .models import (
    LumberingServiceOrder,
    LumberingServiceOutput,
    ShavingsRecord
)


class LumberingServiceOutputInline(admin.TabularInline):
    model = LumberingServiceOutput
    extra = 1
    fields = ['lumber_type', 'quantity_pieces', 'length_feet', 'width_inches', 'thickness_inches', 'board_feet', 'grade']
    readonly_fields = ['board_feet']


class ShavingsRecordInline(admin.TabularInline):
    model = ShavingsRecord
    extra = 1
    fields = ['quantity', 'unit', 'customer_share', 'company_share']


@admin.register(LumberingServiceOrder)
class LumberingServiceOrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer_display',
        'status_display',
        'wood_type',
        'quantity_logs',
        'output_board_feet',
        'total_service_fee_display',
        'received_date',
    ]
    list_filter = ['status', 'received_date', 'shavings_ownership']
    search_fields = ['customer__name', 'wood_type', 'notes']
    readonly_fields = ['actual_output_bf', 'total_service_fee', 'created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Customer & Order Info', {
            'fields': ('customer', 'received_date', 'completed_date', 'status', 'created_by')
        }),
        ('Wood Input', {
            'fields': ('wood_type', 'quantity_logs', 'estimated_board_feet')
        }),
        ('Service Fees', {
            'fields': ('service_fee_per_bf', 'actual_output_bf', 'total_service_fee')
        }),
        ('Shavings Handling', {
            'fields': ('shavings_ownership',)
        }),
        ('Notes & Timestamps', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [LumberingServiceOutputInline, ShavingsRecordInline]
    
    def customer_display(self, obj):
        return obj.customer.name
    customer_display.short_description = 'Customer'
    
    def status_display(self, obj):
        colors = {
            'pending': '#FFA500',
            'in_progress': '#1E90FF',
            'completed': '#228B22',
            'cancelled': '#DC143C',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#666666'),
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def output_board_feet(self, obj):
        bf = obj.actual_output_bf
        return f"{bf} BF" if bf else "—"
    output_board_feet.short_description = 'Actual Output'
    
    def total_service_fee_display(self, obj):
        if obj.total_service_fee:
            return f"₱{obj.total_service_fee:,.2f}"
        return "—"
    total_service_fee_display.short_description = 'Service Fee'


@admin.register(LumberingServiceOutput)
class LumberingServiceOutputAdmin(admin.ModelAdmin):
    list_display = ['lumber_type', 'quantity_pieces', 'dimensions_display', 'board_feet', 'grade', 'service_order']
    list_filter = ['grade', 'recorded_at', 'service_order']
    search_fields = ['lumber_type', 'service_order__customer__name']
    readonly_fields = ['board_feet', 'recorded_at', 'updated_at']
    
    fieldsets = (
        ('Service Order', {
            'fields': ('service_order',)
        }),
        ('Lumber Details', {
            'fields': ('lumber_type', 'quantity_pieces', 'grade')
        }),
        ('Dimensions & Board Feet', {
            'fields': ('length_feet', 'width_inches', 'thickness_inches', 'board_feet')
        }),
        ('Notes & Timestamps', {
            'fields': ('notes', 'recorded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def dimensions_display(self, obj):
        return f"{obj.length_feet}' × {obj.width_inches}\" × {obj.thickness_inches}\""
    dimensions_display.short_description = 'Dimensions'


@admin.register(ShavingsRecord)
class ShavingsRecordAdmin(admin.ModelAdmin):
    list_display = ['service_order', 'quantity_display', 'ownership_display', 'recorded_at']
    list_filter = ['unit', 'recorded_at', 'service_order']
    search_fields = ['service_order__customer__name']
    readonly_fields = ['recorded_at', 'updated_at']
    
    fieldsets = (
        ('Service Order', {
            'fields': ('service_order',)
        }),
        ('Shavings Quantity', {
            'fields': ('quantity', 'unit')
        }),
        ('Ownership', {
            'fields': ('customer_share', 'company_share')
        }),
        ('Notes & Timestamps', {
            'fields': ('notes', 'recorded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def quantity_display(self, obj):
        return f"{obj.quantity} {obj.get_unit_display()}"
    quantity_display.short_description = 'Quantity'
    
    def ownership_display(self, obj):
        return f"Customer: {obj.customer_share}% | Company: {obj.company_share}%"
    ownership_display.short_description = 'Ownership'

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from app_supplier.models import Supplier
from core.models import CustomUser


class WoodType(models.Model):
    """Types of round wood (logs) available for purchase"""
    
    SPECIES_CHOICES = [
        ('hardwood', 'Hardwood'),
        ('softwood', 'Softwood'),
        ('tropical', 'Tropical'),
        ('mixed', 'Mixed Species'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    description = models.TextField(blank=True)
    
    # Standard measurements for this wood type
    default_diameter_inches = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Default log diameter in inches"
    )
    default_length_feet = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Default log length in feet"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Wood Types'
    
    def __str__(self):
        return f"{self.name} ({self.get_species_display()})"


class RoundWoodPurchaseOrder(models.Model):
    """SIMPLIFIED: Purchase order for round wood with no inspections, payment on delivery"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('ordered', 'Ordered'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]
    
    # Order identification
    po_number = models.CharField(
        max_length=50, 
        unique=True,
        blank=True,  # Will be auto-generated
        help_text="Auto-generated PO number"
    )
    po_number_supplier = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Supplier's reference number for this order"
    )
    
    # Parties involved
    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.CASCADE, 
        related_name='round_wood_orders_simple'
    )
    
    # Status tracking
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        db_index=True
    )
    
    # Payment status
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid',
        help_text="Track if supplier has been paid"
    )
    
    # Key dates (SIMPLIFIED: only actual delivery date)
    order_date = models.DateField(default=timezone.now)
    delivery_date = models.DateField(null=True, blank=True, help_text="Actual delivery date")
    
    # Financial information
    total_volume_cubic_feet = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total log volume in cubic feet"
    )
    unit_cost_per_cubic_foot = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    total_amount = models.DecimalField(
        max_digits=14, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Additional information
    notes = models.TextField(blank=True)
    
    # Audit trail (SIMPLIFIED: only created_by, no approved_by)
    created_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='round_wood_orders_simple'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Auto-generate PO number if not provided"""
        if not self.po_number:
            from datetime import datetime
            year = datetime.now().year
            count = RoundWoodPurchaseOrder.objects.filter(
                created_at__year=year
            ).count()
            self.po_number = f"RWPO-{year}-{count + 1:04d}"
        
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Round Wood Purchase Order'
        verbose_name_plural = 'Round Wood Purchase Orders'
        indexes = [
            models.Index(fields=['po_number']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['supplier', '-created_at']),
            models.Index(fields=['payment_status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.po_number} - {self.supplier.company_name}"
    
    def calculate_total(self):
        """Calculate total amount from items"""
        total = Decimal('0')
        for item in self.items.all():
            item.subtotal = item.volume_cubic_feet * self.unit_cost_per_cubic_foot
            item.save()
            total += item.subtotal
        self.total_amount = total
        self.save()
        return total
    
    def mark_as_ordered(self):
        """Mark order as submitted to supplier"""
        self.status = 'ordered'
        self.save()
    
    def mark_as_delivered(self, delivery_date=None):
        """Mark order as delivered and add to inventory"""
        self.status = 'delivered'
        self.delivery_date = delivery_date or timezone.now().date()
        self.payment_status = 'unpaid'  # Ready to pay
        self.save()
        
        # Auto-create/update inventory
        self._update_inventory()
    
    def mark_as_paid(self):
        """Record payment to supplier"""
        self.payment_status = 'paid'
        self.save()
    
    def _update_inventory(self):
        """Auto-update RoundWoodInventory when delivered"""
        from app_round_wood.models import RoundWoodInventory
        
        # Get all unique wood types in this order
        for item in self.items.all():
            inventory, created = RoundWoodInventory.objects.get_or_create(
                wood_type=item.wood_type
            )
            
            # Update stock
            inventory.total_logs_in_stock += item.quantity_logs
            inventory.total_cubic_feet_in_stock += item.volume_cubic_feet
            inventory.total_cost_invested += item.subtotal
            
            # Recalculate average cost
            if inventory.total_cubic_feet_in_stock > 0:
                inventory.average_cost_per_cubic_foot = (
                    inventory.total_cost_invested / inventory.total_cubic_feet_in_stock
                )
            
            inventory.last_stock_in_date = timezone.now().date()
            inventory.save()


class RoundWoodPurchaseOrderItem(models.Model):
    """Individual items (log batches) in a round wood purchase order - SIMPLIFIED"""
    
    purchase_order = models.ForeignKey(
        RoundWoodPurchaseOrder, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    
    wood_type = models.ForeignKey(
        WoodType, 
        on_delete=models.PROTECT,
        related_name='purchase_items_simple'
    )
    
    # Log specifications
    quantity_logs = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of logs in this batch"
    )
    diameter_inches = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Average log diameter in inches"
    )
    length_feet = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Average log length in feet"
    )
    
    # Volume calculation
    volume_cubic_feet = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Total volume calculated from logs"
    )
    
    # Pricing
    unit_cost_per_cubic_foot = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    subtotal = models.DecimalField(
        max_digits=14, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Round Wood Purchase Order Item'
        verbose_name_plural = 'Round Wood Purchase Order Items'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.wood_type.name}"
    
    def calculate_volume(self):
        """
        Calculate volume using log formula:
        Volume (cubic feet) = (π × (diameter/2)² × length × quantity) / 12
        """
        import math
        diameter_feet = self.diameter_inches / 12
        radius_feet = diameter_feet / 2
        volume_per_log = math.pi * (radius_feet ** 2) * float(self.length_feet)
        total_volume = volume_per_log * self.quantity_logs
        return total_volume
    
    def calculate_subtotal(self):
        """Calculate line item subtotal"""
        self.subtotal = self.volume_cubic_feet * self.unit_cost_per_cubic_foot
        return self.subtotal


class RoundWoodInventory(models.Model):
    """Tracks stocked round wood in inventory"""
    
    wood_type = models.OneToOneField(
        WoodType, 
        on_delete=models.CASCADE, 
        related_name='round_wood_inventory'
    )
    
    # Current stock
    total_logs_in_stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    total_cubic_feet_in_stock = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Cost tracking
    total_cost_invested = models.DecimalField(
        max_digits=14, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total cost of all stocked round wood"
    )
    average_cost_per_cubic_foot = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Warehouse location
    warehouse_location = models.CharField(
        max_length=200, 
        blank=True,
        help_text="e.g., Yard A, Section B, Stack 3"
    )
    
    last_updated = models.DateTimeField(auto_now=True)
    last_stock_in_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Round Wood Inventory'
        verbose_name_plural = 'Round Wood Inventories'
    
    def __str__(self):
        return f"{self.wood_type.name} - {self.total_logs_in_stock} logs"

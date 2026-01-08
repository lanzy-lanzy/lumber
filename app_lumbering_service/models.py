from django.db import models
from django.core.validators import MinValueValidator, DecimalValidator
from django.utils import timezone
from decimal import Decimal
from app_sales.models import Customer
from core.models import CustomUser


class LumberingServiceOrder(models.Model):
    """Customer-owned wood received for lumbering service"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Customer information
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    received_date = models.DateField(default=timezone.now)
    completed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Customer's wood input
    wood_type = models.CharField(max_length=100, help_text="Type of wood (Mahogany, Pine, etc.)")
    quantity_logs = models.IntegerField(validators=[MinValueValidator(1)])
    estimated_board_feet = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Initial estimate of board feet"
    )
    
    # Service details
    service_fee_per_bf = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('5.00'),
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Service fee per board foot"
    )
    total_service_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Calculated from actual output × fee per BF"
    )
    
    # Shavings/palaras handling
    SHAVINGS_OWNERSHIP_CHOICES = [
        ('customer', 'Customer'),
        ('lumber_company', 'Lumber Company'),
        ('shared', 'Shared (50/50)'),
    ]
    shavings_ownership = models.CharField(
        max_length=20,
        choices=SHAVINGS_OWNERSHIP_CHOICES,
        default='lumber_company'
    )
    
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lumbering Service Order'
        verbose_name_plural = 'Lumbering Service Orders'
    
    def __str__(self):
        return f"Lumbering Service #{self.pk} - {self.customer.name} ({self.received_date})"
    
    def calculate_service_fee(self):
        """Calculate total service fee based on actual output"""
        if self.actual_output_bf:
            self.total_service_fee = self.actual_output_bf * self.service_fee_per_bf
            return self.total_service_fee
        return None
    
    @property
    def actual_output_bf(self):
        """Get total actual board feet from all output records"""
        output = self.outputs.aggregate(models.Sum('board_feet'))
        return output.get('board_feet__sum') or Decimal('0')


class LumberingServiceOutput(models.Model):
    """Lumber output from customer's wood"""
    
    service_order = models.ForeignKey(
        LumberingServiceOrder,
        on_delete=models.CASCADE,
        related_name='outputs'
    )
    
    # Output lumber details
    lumber_type = models.CharField(
        max_length=100,
        help_text="Type of lumber produced (2x4, 1x12, etc.)"
    )
    quantity_pieces = models.IntegerField(validators=[MinValueValidator(1)])
    length_feet = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    width_inches = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    thickness_inches = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Board feet calculation: (length × width × thickness / 12) × quantity
    # BF = (length_ft × width_in × thickness_in / 12) × quantity
    board_feet = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Quality grading (optional)
    GRADE_CHOICES = [
        ('select', 'Select'),
        ('common1', 'Common #1'),
        ('common2', 'Common #2'),
        ('common3', 'Common #3'),
    ]
    grade = models.CharField(
        max_length=20,
        choices=GRADE_CHOICES,
        default='common1',
        blank=True
    )
    
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Lumbering Service Output'
        verbose_name_plural = 'Lumbering Service Outputs'
    
    def __str__(self):
        return f"{self.lumber_type} - {self.board_feet} BF"
    
    def calculate_board_feet(self):
        """Calculate board feet: (length × width × thickness / 12) × quantity"""
        if all([self.length_feet, self.width_inches, self.thickness_inches, self.quantity_pieces]):
            bf_per_piece = (self.length_feet * self.width_inches * self.thickness_inches) / Decimal('12')
            self.board_feet = bf_per_piece * self.quantity_pieces
            return self.board_feet
        return None
    
    def save(self, *args, **kwargs):
        # Auto-calculate board feet if not set
        if not self.board_feet:
            self.calculate_board_feet()
        super().save(*args, **kwargs)
        # Update parent service order fee
        self.service_order.calculate_service_fee()
        self.service_order.save()


class ShavingsRecord(models.Model):
    """Record of wood shavings (palaras) from lumbering service"""
    
    service_order = models.ForeignKey(
        LumberingServiceOrder,
        on_delete=models.CASCADE,
        related_name='shavings'
    )
    
    # Weight or volume
    UNIT_CHOICES = [
        ('kg', 'Kilograms'),
        ('tons', 'Tons'),
        ('cubic_meters', 'Cubic Meters'),
        ('bags', 'Bags'),
    ]
    
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='kg')
    
    # Ownership split
    customer_share = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0'),
        validators=[MinValueValidator(Decimal('0')), MinValueValidator(Decimal('100'))],
        help_text="Customer's percentage share (0-100)"
    )
    company_share = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0'),
        validators=[MinValueValidator(Decimal('0')), MinValueValidator(Decimal('100'))],
        help_text="Company's percentage share (0-100)"
    )
    
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Shavings Record'
        verbose_name_plural = 'Shavings Records'
    
    def __str__(self):
        return f"Shavings - {self.quantity} {self.get_unit_display()}"
    
    def save(self, *args, **kwargs):
        # Ensure customer and company shares add up to 100
        if self.customer_share + self.company_share != Decimal('100'):
            # Auto-adjust based on service order's shavings_ownership
            if self.service_order.shavings_ownership == 'customer':
                self.customer_share = Decimal('100')
                self.company_share = Decimal('0')
            elif self.service_order.shavings_ownership == 'lumber_company':
                self.customer_share = Decimal('0')
                self.company_share = Decimal('100')
            else:  # shared
                self.customer_share = Decimal('50')
                self.company_share = Decimal('50')
        super().save(*args, **kwargs)

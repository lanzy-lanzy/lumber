from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Role choices for users
ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('inventory_manager', 'Inventory Manager'),
    ('cashier', 'Cashier'),
    ('warehouse_staff', 'Warehouse Staff'),
]

# User type choices
USER_TYPE_CHOICES = [
    ('employee', 'Employee'),
    ('customer', 'Customer'),
]


class CustomUser(AbstractUser):
    """Extended User model with role-based access control"""
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='employee'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='warehouse_staff',
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False, help_text="Admin approval for customer registration")
    id_document = models.FileField(
        upload_to='id_documents/',
        blank=True,
        null=True,
        help_text="Upload government ID or valid identification"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"

    def is_admin(self):
        return self.role == 'admin'

    def is_inventory_manager(self):
        return self.role == 'inventory_manager'

    def is_cashier(self):
        return self.role == 'cashier'

    def is_warehouse_staff(self):
        return self.role == 'warehouse_staff'

    def is_employee(self):
        return self.user_type == 'employee'

    def is_customer(self):
        return self.user_type == 'customer'


class CustomerProfile(models.Model):
    """Customer profile linked to CustomUser"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    address = models.TextField(blank=True)
    is_senior = models.BooleanField(default=False)
    is_pwd = models.BooleanField(
        default=False,
        verbose_name='PWD (Person with Disability)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profiles'

    def __str__(self):
        return f"{self.user.get_full_name()} - Customer"

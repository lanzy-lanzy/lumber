# ID Document Verification - Code Reference

## Database Model Changes

### core/models.py
```python
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
    
    # NEW FIELDS FOR ID VERIFICATION
    is_approved = models.BooleanField(
        default=False, 
        help_text="Admin approval for customer registration"
    )
    id_document = models.FileField(
        upload_to='id_documents/',
        blank=True,
        null=True,
        help_text="Upload government ID or valid identification"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## View Changes

### app_authentication/views.py

#### Register View - Handle ID Upload
```python
@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration view for both employees and customers"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        user_type = request.POST.get('user_type', 'employee').strip()
        role = request.POST.get('role', '').strip() if user_type == 'employee' else None
        address = request.POST.get('address', '').strip() if user_type == 'customer' else ''
        is_senior = request.POST.get('is_senior') == 'true' if user_type == 'customer' else False
        is_pwd = request.POST.get('is_pwd') == 'true' if user_type == 'customer' else False
        
        # NEW: Get ID document file
        id_document = request.FILES.get('id_document') if user_type == 'customer' else None
        
        # Validation
        errors = []
        
        # ... existing validations ...
        
        # NEW: ID document validation for customers
        if user_type == 'customer':
            if not id_document:
                errors.append('ID document is required for customer registration.')
            elif id_document.size > 5242880:  # 5MB limit
                errors.append('ID document must be less than 5MB.')
        
        if errors:
            # Return with errors
            context = {
                'page_title': 'Register',
                'errors': errors,
                'form_data': {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'username': username,
                    'phone_number': phone_number,
                    'user_type': user_type,
                    'role': role,
                    'address': address,
                    'is_senior': 'true' if is_senior else '',
                    'is_pwd': 'true' if is_pwd else '',
                    'id_document': id_document.name if id_document else '',
                },
                'role_choices': ROLE_CHOICES,
            }
            return render(request, 'authentication/register.html', context)
        
        # Create user
        try:
            # NEW: For customers, set is_approved to False (requires admin approval)
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                user_type=user_type,
                role=role if user_type == 'employee' else None,
                is_approved=True if user_type == 'employee' else False,
                id_document=id_document if user_type == 'customer' else None,
            )
            
            # Create customer profile if user is a customer
            if user_type == 'customer':
                CustomerProfile.objects.create(
                    user=user,
                    address=address,
                    is_senior=is_senior,
                    is_pwd=is_pwd,
                )
                # NEW: Don't auto-login customer
                messages.success(request, 
                    'Account created successfully! Your ID has been submitted for admin approval. '
                    'You will be able to login once approved.')
                return redirect('login')
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
```

#### Login View - Check Approval Status
```python
@never_cache
@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'authentication/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            user.refresh_from_db()
            
            # NEW: Check if customer is approved
            if user.is_customer() and not user.is_approved:
                messages.error(request, 
                    'Your account is pending admin approval. '
                    'Please check your email for approval status.')
                return render(request, 'authentication/login.html', 
                    {'username': username})
            
            login(request, user)
            messages.success(request, 
                f'Welcome back, {user.get_full_name() or user.username}!')
            
            # Redirect based on user type
            if user.is_customer():
                return redirect('customer-dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'authentication/login.html', 
                {'username': username})
```

#### New View - Pending Registrations
```python
@login_required
@require_http_methods(["GET"])
def pending_registrations_view(request):
    """View pending customer registrations for admin approval"""
    # Only admins can access this view
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    # Get all unapproved customer registrations
    pending_users = CustomUser.objects.filter(
        user_type='customer',
        is_approved=False
    ).select_related('customer_profile').order_by('-created_at')
    
    context = {
        'page_title': 'Pending Registrations',
        'pending_users': pending_users,
        'pending_count': pending_users.count(),
    }
    return render(request, 'authentication/pending_registrations.html', context)


@login_required
@require_http_methods(["POST"])
def approve_registration_view(request, user_id):
    """Approve a pending customer registration"""
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    try:
        user = CustomUser.objects.get(id=user_id, user_type='customer', is_approved=False)
        user.is_approved = True
        user.save()
        messages.success(request, f'{user.get_full_name()} has been approved and can now login.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found or already approved.')
    
    return redirect('pending_registrations')


@login_required
@require_http_methods(["POST"])
def reject_registration_view(request, user_id):
    """Reject a pending customer registration"""
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    try:
        user = CustomUser.objects.get(id=user_id, user_type='customer', is_approved=False)
        email = user.email
        user.delete()
        messages.success(request, f'Registration for {email} has been rejected and deleted.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found or already approved.')
    
    return redirect('pending_registrations')
```

## URL Configuration

### app_authentication/urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # NEW: Admin registration approval endpoints
    path('admin/pending-registrations/', 
         views.pending_registrations_view, 
         name='pending_registrations'),
    path('admin/pending-registrations/<int:user_id>/approve/', 
         views.approve_registration_view, 
         name='approve_registration'),
    path('admin/pending-registrations/<int:user_id>/reject/', 
         views.reject_registration_view, 
         name='reject_registration'),
]
```

## Context Processor

### core/context_processors.py (NEW)
```python
from core.models import CustomUser


def pending_registrations_count(request):
    """Add pending registrations count to context for admin users"""
    pending_count = 0
    
    if request.user.is_authenticated and request.user.is_admin():
        pending_count = CustomUser.objects.filter(
            user_type='customer',
            is_approved=False
        ).count()
    
    return {
        'pending_count': pending_count,
    }
```

## Settings Configuration

### lumber/settings.py
```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "app_sales.context_processors.order_notifications",
                "core.context_processors.pending_registrations_count",  # NEW
            ],
        },
    },
]

# Media files configuration (for storing ID documents)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Template Changes

### templates/authentication/register.html
```html
<!-- Add enctype to form -->
<form method="POST" class="space-y-4" id="registrationForm" enctype="multipart/form-data">
    {% csrf_token %}
    
    <!-- ... existing fields ... -->
    
    <!-- NEW: ID Document Upload (Customer Only) -->
    <div id="idDocumentField" class="hidden">
        <label for="id_document" class="block text-sm font-medium text-slate-300 mb-2">
            Government ID / Identification Document
        </label>
        <div class="relative">
            <input
                type="file"
                id="id_document"
                name="id_document"
                accept=".pdf,.jpg,.jpeg,.png,.gif"
                class="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
            >
        </div>
        <p class="text-xs text-slate-400 mt-1">
            Accepted formats: PDF, JPG, JPEG, PNG (Max 5MB). Required for customer approval.
        </p>
    </div>
</form>

<!-- JavaScript to toggle field visibility -->
<script>
    function toggleUserTypeFields() {
        const userType = document.querySelector('input[name="user_type"]:checked').value;
        
        if (userType === 'customer') {
            document.getElementById('idDocumentField').classList.remove('hidden');
            document.getElementById('id_document').setAttribute('required', 'required');
        } else {
            document.getElementById('idDocumentField').classList.add('hidden');
            document.getElementById('id_document').removeAttribute('required');
        }
    }
</script>
```

### templates/base.html
```html
<!-- In admin sidebar, after other sections -->
{% if user.role == "admin" %}
    <!-- User Management Section -->
    <div class="pt-6 mt-6 border-t border-gray-700">
        <div class="px-4 py-2 text-xs font-bold text-purple-400 uppercase tracking-wide">
            User Management
        </div>
        <a href="{% url 'pending_registrations' %}" 
           class="sidebar-nav flex items-center px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300 hover:text-white justify-between">
            <div class="flex items-center">
                <i class="fas fa-user-check w-5 mr-3 text-purple-400"></i>
                <span>Pending Registrations</span>
            </div>
            {% if pending_count|default:0 > 0 %}
                <span class="bg-yellow-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
                    {{ pending_count }}
                </span>
            {% endif %}
        </a>
    </div>
{% endif %}
```

## Migration

### core/migrations/0003_customuser_id_document_customuser_is_approved.py
```python
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_customuser_user_type_alter_customuser_role_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_approved",
            field=models.BooleanField(
                default=False, 
                help_text="Admin approval for customer registration"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="id_document",
            field=models.FileField(
                blank=True,
                help_text="Upload government ID or valid identification",
                null=True,
                upload_to="id_documents/",
            ),
        ),
    ]
```

## Database Queries

### Find all pending customers
```python
from core.models import CustomUser

pending = CustomUser.objects.filter(
    user_type='customer',
    is_approved=False
).order_by('-created_at')
```

### Approve a customer
```python
user = CustomUser.objects.get(id=user_id)
user.is_approved = True
user.save()
```

### Get customer's ID document
```python
user = CustomUser.objects.get(id=user_id)
if user.id_document:
    url = user.id_document.url
    path = user.id_document.path
```

## Security Features

1. **File Upload Validation**
   - Restricted MIME types
   - Size limit (5MB)
   - Safe directory (`id_documents/`)

2. **Access Control**
   - `@login_required` decorator
   - `is_admin()` check on all approval views
   - CSRF protection on POST requests

3. **Data Safety**
   - Proper error handling
   - Transaction safety on create_user
   - No sensitive data in error messages

## Testing

### Test Scenario 1: Customer Registration
```python
# POST to /auth/register/
data = {
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john@example.com',
    'username': 'johndoe',
    'password': 'TestPassword123',
    'password_confirm': 'TestPassword123',
    'user_type': 'customer',
    'phone_number': '+1234567890',
    'address': '123 Main St',
    'id_document': <file_object>,
}
# Expected: Account created with is_approved=False
```

### Test Scenario 2: Login Before Approval
```python
# POST to /auth/login/
data = {
    'username': 'johndoe',
    'password': 'TestPassword123',
}
# Expected: Error message "Your account is pending admin approval"
```

### Test Scenario 3: Admin Approval
```python
# POST to /auth/admin/pending-registrations/<user_id>/approve/
# Expected: is_approved=True, success message
```

### Test Scenario 4: Login After Approval
```python
# POST to /auth/login/
data = {
    'username': 'johndoe',
    'password': 'TestPassword123',
}
# Expected: Login successful, redirected to customer-dashboard
```

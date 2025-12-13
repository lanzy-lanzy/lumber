from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import CustomUser
from core.serializers import UserSerializer, UserCreateSerializer


@require_http_methods(["GET"])
def home(request):
    """Landing page - main entry point"""
    # If user is authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Show landing page to unauthenticated users
    context = {}
    return render(request, 'landing.html', context)


@never_cache
@login_required
@require_http_methods(["GET"])
def dashboard(request):
    """Dashboard page - employees only"""
    # Refresh user from database to ensure clean session state
    request.user.refresh_from_db()
    
    # Customers should not access this view - redirect them
    if request.user.is_customer():
        return redirect('customer-dashboard')
    
    # Check if user has a valid role, if not set default
    if not request.user.role and request.user.is_employee():
        request.user.role = 'warehouse_staff'
        request.user.save()
    
    # Employee dashboard
    context = {
        'user': request.user,
        'user_role': request.user.role,
    }
    return render(request, 'dashboard.html', context)


@never_cache
@login_required
@require_http_methods(["GET"])
def customer_dashboard(request):
    """Customer dashboard view - customers only"""
    import sys
    print(f"DEBUG: customer_dashboard accessed", file=sys.stderr)
    print(f"DEBUG: user={request.user.username}, is_authenticated={request.user.is_authenticated}", file=sys.stderr)
    print(f"DEBUG: is_customer={request.user.is_customer()}", file=sys.stderr)
    
    # Refresh user from database to ensure clean session state
    request.user.refresh_from_db()
    
    # Only allow customers
    if not request.user.is_customer():
        print(f"DEBUG: User is not a customer, redirecting to dashboard", file=sys.stderr)
        return redirect('dashboard')
    
    print(f"DEBUG: Rendering customer dashboard", file=sys.stderr)
    
    from app_sales.models import SalesOrder, Customer as SalesCustomer
    from django.db.models import Sum, Count
    
    # Get customer's sales orders if they have a linked customer record
    sales_orders = SalesOrder.objects.none()
    total_spent = 0
    order_count = 0
    
    try:
        # Try to find customer record by email
        sales_customer = SalesCustomer.objects.filter(email=request.user.email).first()
        if sales_customer:
            sales_orders = sales_customer.sales_orders.all().order_by('-created_at')[:10]
            stats = sales_customer.sales_orders.aggregate(
                total=Sum('total_amount'),
                count=Count('id')
            )
            total_spent = stats['total'] or 0
            order_count = stats['count'] or 0
    except Exception as e:
        print(f"DEBUG: Exception in customer_dashboard: {e}", file=sys.stderr)
        pass
    
    context = {
        'user': request.user,
        'customer_profile': getattr(request.user, 'customer_profile', None),
        'sales_orders': sales_orders,
        'total_spent': total_spent,
        'order_count': order_count,
    }
    return render(request, 'customer/dashboard.html', context)


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint for user management"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user information"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_role(self, request):
        """Get users by role"""
        role = request.query_params.get('role')
        if not role:
            return Response({'error': 'role parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        users = CustomUser.objects.filter(role=role)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from app_inventory.models import LumberProduct, LumberCategory, Inventory
from app_sales.models import Customer as SalesCustomer, SalesOrder


@login_required
@require_http_methods(["GET"])
def customer_browse_products(request):
    """Browse products as a customer"""
    if not request.user.is_customer():
        return redirect('dashboard')
    
    # Get filter parameters
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-created_at')
    
    # Start with all active products
    products = LumberProduct.objects.filter(is_active=True).select_related('category', 'inventory')
    
    # Apply category filter
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Apply search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Apply sorting
    if sort_by in ['name', '-name', 'price_per_board_foot', '-price_per_board_foot', 'created_at', '-created_at']:
        products = products.order_by(sort_by)
    else:
        products = products.order_by('-created_at')
    
    # Get all categories for filter
    categories = LumberCategory.objects.all().order_by('name')
    
    # Get customer profile
    customer_profile = getattr(request.user, 'customer_profile', None)
    
    # Get customer sales info
    sales_orders = SalesOrder.objects.none()
    order_count = 0
    total_spent = 0
    
    try:
        sales_customer = SalesCustomer.objects.filter(email=request.user.email).first()
        if sales_customer:
            sales_orders = sales_customer.sales_orders.all().order_by('-created_at')[:5]
            stats = sales_customer.sales_orders.aggregate(
                total=Sum('total_amount'),
                count=Count('id')
            )
            total_spent = stats['total'] or 0
            order_count = stats['count'] or 0
    except:
        pass
    
    context = {
        'user': request.user,
        'customer_profile': customer_profile,
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
        'sort_by': sort_by,
        'sales_orders': sales_orders,
        'order_count': order_count,
        'total_spent': total_spent,
    }
    
    return render(request, 'customer/browse_products.html', context)


@login_required
@require_http_methods(["GET"])
def customer_product_detail(request, product_id):
    """View product details as a customer"""
    if not request.user.is_customer():
        return redirect('dashboard')
    
    product = get_object_or_404(LumberProduct, id=product_id, is_active=True)
    inventory = getattr(product, 'inventory', None)
    
    # Get related products from same category
    related_products = LumberProduct.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Get customer profile
    customer_profile = getattr(request.user, 'customer_profile', None)
    
    context = {
        'user': request.user,
        'customer_profile': customer_profile,
        'product': product,
        'inventory': inventory,
        'related_products': related_products,
    }
    
    return render(request, 'customer/product_detail.html', context)


@login_required
@require_http_methods(["GET"])
def customer_my_orders(request):
    """View customer's orders"""
    if not request.user.is_customer():
        return redirect('dashboard')
    
    # Get customer's sales orders
    sales_orders = SalesOrder.objects.none()
    total_spent = 0
    order_count = 0
    
    try:
        sales_customer = SalesCustomer.objects.filter(email=request.user.email).first()
        if sales_customer:
            sales_orders = sales_customer.sales_orders.all().order_by('-created_at')
            stats = sales_customer.sales_orders.aggregate(
                total=Sum('total_amount'),
                count=Count('id')
            )
            total_spent = stats['total'] or 0
            order_count = stats['count'] or 0
    except:
        pass
    
    # Get customer profile
    customer_profile = getattr(request.user, 'customer_profile', None)
    
    context = {
        'user': request.user,
        'customer_profile': customer_profile,
        'sales_orders': sales_orders,
        'total_spent': total_spent,
        'order_count': order_count,
    }
    
    return render(request, 'customer/my_orders.html', context)


@login_required
@require_http_methods(["GET"])
def customer_order_detail(request, order_id):
    """View order details"""
    if not request.user.is_customer():
        return redirect('dashboard')
    
    # Try to find the order linked to this customer's email
    sales_order = get_object_or_404(SalesOrder, id=order_id)
    
    # Verify the order belongs to a customer with the same email
    if sales_order.customer.email != request.user.email:
        return redirect('customer-dashboard')
    
    # Get customer profile
    customer_profile = getattr(request.user, 'customer_profile', None)
    
    context = {
        'user': request.user,
        'customer_profile': customer_profile,
        'order': sales_order,
        'order_items': sales_order.sales_order_items.all(),
    }
    
    return render(request, 'customer/order_detail.html', context)


@login_required
@require_http_methods(["GET"])
def customer_profile(request):
    """View customer profile"""
    if not request.user.is_customer():
        return redirect('dashboard')
    
    # Get customer profile
    customer_profile = getattr(request.user, 'customer_profile', None)
    
    # Get customer sales info
    sales_orders = SalesOrder.objects.none()
    order_count = 0
    total_spent = 0
    
    try:
        sales_customer = SalesCustomer.objects.filter(email=request.user.email).first()
        if sales_customer:
            stats = sales_customer.sales_orders.aggregate(
                total=Sum('total_amount'),
                count=Count('id')
            )
            total_spent = stats['total'] or 0
            order_count = stats['count'] or 0
    except:
        pass
    
    context = {
        'user': request.user,
        'customer_profile': customer_profile,
        'order_count': order_count,
        'total_spent': total_spent,
    }
    
    return render(request, 'customer/profile.html', context)


@login_required
@require_http_methods(["GET"])
def customer_shopping_cart(request):
    """View shopping cart"""
    if not request.user.is_customer():
        return redirect('dashboard')
    
    # Get customer profile
    customer_profile = getattr(request.user, 'customer_profile', None)
    
    context = {
        'user': request.user,
        'customer_profile': customer_profile,
    }
    
    return render(request, 'customer/shopping_cart.html', context)

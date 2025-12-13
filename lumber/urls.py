from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from core.views import UserViewSet
from app_inventory.views import (
    LumberCategoryViewSet, LumberProductViewSet, InventoryViewSet, 
    StockTransactionViewSet, InventoryReportViewSet, AdjustmentViewSet
)
from app_sales.views import CustomerViewSet, SalesOrderViewSet, ReceiptViewSet
from app_sales.cart_views import ShoppingCartViewSet
from app_sales.pos import POSViewSet
from app_sales.report_views import SalesReportViewSet
from app_sales.confirmation_views import OrderConfirmationViewSet, NotificationViewSet
from app_delivery.views import DeliveryViewSet
from app_delivery.report_views import DeliveryReportViewSet
from app_delivery.warehouse import WarehouseViewSet
from app_supplier.views import SupplierViewSet, PurchaseOrderViewSet, SupplierPriceHistoryViewSet
from app_supplier.report_views import SupplierReportViewSet
from app_dashboard.views import DashboardMetricViewSet

# Create router and register viewsets
router = DefaultRouter()

# Core
router.register(r'users', UserViewSet, basename='user')

# Inventory
router.register(r'categories', LumberCategoryViewSet, basename='category')
router.register(r'products', LumberProductViewSet, basename='product')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'stock-transactions', StockTransactionViewSet, basename='stock-transaction')
router.register(r'adjustments', AdjustmentViewSet, basename='adjustment')
router.register(r'inventory-reports', InventoryReportViewSet, basename='inventory-report')

# Sales
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'sales-orders', SalesOrderViewSet, basename='sales-order')
router.register(r'receipts', ReceiptViewSet, basename='receipt')
router.register(r'cart', ShoppingCartViewSet, basename='shopping-cart')
router.register(r'pos', POSViewSet, basename='pos')
router.register(r'sales-reports', SalesReportViewSet, basename='sales-report')
router.register(r'confirmations', OrderConfirmationViewSet, basename='confirmation')
router.register(r'notifications', NotificationViewSet, basename='notification')

# Delivery
router.register(r'deliveries', DeliveryViewSet, basename='delivery')
router.register(r'delivery-reports', DeliveryReportViewSet, basename='delivery-report')
router.register(r'warehouse', WarehouseViewSet, basename='warehouse')

# Supplier
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'purchase-orders', PurchaseOrderViewSet, basename='purchase-order')
router.register(r'supplier-prices', SupplierPriceHistoryViewSet, basename='supplier-price')
router.register(r'supplier-reports', SupplierReportViewSet, basename='supplier-report')

# Dashboard
router.register(r'metrics', DashboardMetricViewSet, basename='metric')

urlpatterns = [
    path('', include('core.urls')),
    path('auth/', include('app_authentication.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('inventory/management/', include('app_inventory.management_urls')),
    path('', include('app_sales.notification_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

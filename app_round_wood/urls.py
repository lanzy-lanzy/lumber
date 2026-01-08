from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'round_wood'

router = DefaultRouter()
router.register(r'wood-types', views.WoodTypeViewSet, basename='wood-type')
router.register(r'round-wood-purchases', views.RoundWoodPurchaseOrderViewSet, basename='round-wood-po')
router.register(r'round-wood-items', views.RoundWoodPurchaseOrderItemViewSet, basename='round-wood-po-item')
router.register(r'round-wood-inventory', views.RoundWoodInventoryViewSet, basename='round-wood-inventory')

urlpatterns = [
    path('', include(router.urls)),
]

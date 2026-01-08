from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import WoodType, RoundWoodPurchaseOrder, RoundWoodPurchaseOrderItem, RoundWoodInventory
from .serializers_simplified import (
    WoodTypeSerializer,
    RoundWoodPurchaseOrderListSerializer,
    RoundWoodPurchaseOrderDetailSerializer,
    RoundWoodPurchaseOrderSimpleSerializer,
    RoundWoodPurchaseOrderItemSerializer,
    RoundWoodInventorySerializer
)


class WoodTypeViewSet(viewsets.ModelViewSet):
    """Wood type management"""
    queryset = WoodType.objects.all()
    serializer_class = WoodTypeSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'species']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class RoundWoodPurchaseOrderViewSet(viewsets.ModelViewSet):
    """
    SIMPLIFIED Round Wood Purchase Order Management
    
    Workflow:
    1. Create (Draft)
    2. /order/ - Mark as ordered
    3. /deliver/ - Mark as delivered + add to inventory
    4. /pay/ - Mark as paid
    """
    queryset = RoundWoodPurchaseOrder.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]
    search_fields = ['po_number', 'po_number_supplier', 'supplier__company_name']
    ordering_fields = ['po_number', 'status', 'payment_status', 'order_date', 'delivery_date', 'total_amount']
    ordering = ['-created_at']
    filterset_fields = ['status', 'payment_status', 'supplier', 'order_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RoundWoodPurchaseOrderListSerializer
        elif self.action == 'create':
            return RoundWoodPurchaseOrderSimpleSerializer
        else:
            return RoundWoodPurchaseOrderDetailSerializer
    
    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def order(self, request, pk=None):
        """Mark purchase order as ordered (submitted to supplier)"""
        po = self.get_object()
        
        if po.status != 'draft':
            return Response(
                {'error': 'Only draft orders can be marked as ordered'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not po.items.exists():
            return Response(
                {'error': 'Order must have at least one item'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        po.mark_as_ordered()
        serializer = self.get_serializer(po)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deliver(self, request, pk=None):
        """Mark order as delivered and add to inventory"""
        po = self.get_object()
        
        if po.status != 'ordered':
            return Response(
                {'error': 'Only ordered items can be marked as delivered'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get delivery date from request or use today
        delivery_date = request.data.get('delivery_date')
        
        po.mark_as_delivered(delivery_date=delivery_date)
        serializer = self.get_serializer(po)
        
        return Response({
            'message': 'Order delivered and added to inventory',
            'order': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """Mark order as paid to supplier"""
        po = self.get_object()
        
        if po.status != 'delivered':
            return Response(
                {'error': 'Only delivered orders can be marked as paid'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if po.payment_status == 'paid':
            return Response(
                {'error': 'Order is already marked as paid'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        po.mark_as_paid()
        serializer = self.get_serializer(po)
        
        return Response({
            'message': 'Order marked as paid',
            'order': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def pending_delivery(self, request):
        """Get all orders awaiting delivery"""
        orders = self.queryset.filter(status='ordered')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_payment(self, request):
        """Get all delivered orders awaiting payment"""
        orders = self.queryset.filter(status='delivered', payment_status='unpaid')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics"""
        total_orders = self.queryset.count()
        total_volume = self.queryset.aggregate(
            total=models.Sum('total_volume_cubic_feet')
        )['total'] or 0
        total_amount = self.queryset.aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0
        
        status_breakdown = {}
        for status_choice, _ in RoundWoodPurchaseOrder.STATUS_CHOICES:
            status_breakdown[status_choice] = self.queryset.filter(
                status=status_choice
            ).count()
        
        return Response({
            'total_orders': total_orders,
            'total_volume_cubic_feet': float(total_volume),
            'total_amount': float(total_amount),
            'status_breakdown': status_breakdown,
            'pending_delivery': self.queryset.filter(status='ordered').count(),
            'pending_payment': self.queryset.filter(
                status='delivered', 
                payment_status='unpaid'
            ).count(),
        })


class RoundWoodPurchaseOrderItemViewSet(viewsets.ModelViewSet):
    """Manage individual items in purchase orders"""
    queryset = RoundWoodPurchaseOrderItem.objects.all()
    serializer_class = RoundWoodPurchaseOrderItemSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['purchase_order', 'wood_type']
    ordering_fields = ['quantity_logs', 'volume_cubic_feet', 'subtotal']
    ordering = ['created_at']
    
    def perform_create(self, serializer):
        """Auto-calculate volume and update PO total"""
        item = serializer.save()
        
        # Recalculate PO total
        po = item.purchase_order
        po.calculate_total()
    
    def perform_update(self, serializer):
        """Auto-calculate volume and update PO total"""
        item = serializer.save()
        
        # Recalculate PO total
        po = item.purchase_order
        po.calculate_total()
    
    def perform_destroy(self, instance):
        """Recalculate PO total when item deleted"""
        po = instance.purchase_order
        instance.delete()
        po.calculate_total()


class RoundWoodInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """View current round wood inventory (read-only)"""
    queryset = RoundWoodInventory.objects.all()
    serializer_class = RoundWoodInventorySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['wood_type']
    ordering_fields = ['total_logs_in_stock', 'total_cubic_feet_in_stock', 'total_cost_invested']
    ordering = ['wood_type__name']
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get inventory summary"""
        inventories = self.queryset
        
        total_logs = sum(inv.total_logs_in_stock for inv in inventories)
        total_cubic_feet = sum(float(inv.total_cubic_feet_in_stock) for inv in inventories)
        total_cost = sum(float(inv.total_cost_invested) for inv in inventories)
        
        return Response({
            'total_logs_in_stock': total_logs,
            'total_cubic_feet_in_stock': float(total_cubic_feet),
            'total_cost_invested': float(total_cost),
            'wood_types_in_stock': len(inventories),
            'average_cost_per_cubic_foot': float(total_cost / total_cubic_feet) if total_cubic_feet > 0 else 0,
        })
    
    @action(detail=True, methods=['get'])
    def valuation(self, request, pk=None):
        """Get valuation for specific wood type"""
        inventory = self.get_object()
        
        return Response({
            'wood_type': inventory.wood_type.name,
            'total_logs': inventory.total_logs_in_stock,
            'total_cubic_feet': float(inventory.total_cubic_feet_in_stock),
            'total_cost_invested': float(inventory.total_cost_invested),
            'average_cost_per_cubic_foot': float(inventory.average_cost_per_cubic_foot),
            'warehouse_location': inventory.warehouse_location,
            'last_stock_in_date': inventory.last_stock_in_date,
        })


# Import models for aggregation
from django.db import models

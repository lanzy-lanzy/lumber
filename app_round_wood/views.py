from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import models
from .models import WoodType, RoundWoodPurchase, RoundWoodInventory
from .serializers import (
    WoodTypeSerializer,
    RoundWoodPurchaseSerializer,
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


class RoundWoodPurchaseViewSet(viewsets.ModelViewSet):
    """
    SIMPLIFIED Round Wood Purchase Management
    
    Single-user direct purchasing system
    Workflow: Purchase → Encode Details → Save Record → Update Inventory
    """
    queryset = RoundWoodPurchase.objects.all().select_related('supplier', 'wood_type').order_by('-purchase_date')
    serializer_class = RoundWoodPurchaseSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['supplier__company_name', 'wood_type__name', 'notes']
    ordering_fields = ['purchase_date', 'status', 'total_cost', 'quantity_logs']
    ordering = ['-purchase_date']
    filterset_fields = ['status', 'supplier', 'wood_type', 'purchase_date']
    
    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark purchase as completed and add to inventory"""
        purchase = self.get_object()
        
        if purchase.status == 'completed':
            return Response(
                {'error': 'Purchase is already completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if purchase.status == 'cancelled':
            return Response(
                {'error': 'Cannot complete a cancelled purchase'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        purchase.mark_completed()
        serializer = self.get_serializer(purchase)
        
        return Response({
            'message': 'Purchase completed and added to inventory',
            'purchase': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a purchase"""
        purchase = self.get_object()
        
        if purchase.status == 'completed':
            return Response(
                {'error': 'Cannot cancel a completed purchase'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        purchase.status = 'cancelled'
        purchase.save()
        serializer = self.get_serializer(purchase)
        
        return Response({
            'message': 'Purchase cancelled',
            'purchase': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending purchases"""
        purchases = self.queryset.filter(status='pending')
        serializer = self.get_serializer(purchases, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics"""
        total_purchases = self.queryset.count()
        total_volume = self.queryset.filter(status='completed').aggregate(
            total=models.Sum('volume_cubic_feet')
        )['total'] or 0
        total_spent = self.queryset.filter(status='completed').aggregate(
            total=models.Sum('total_cost')
        )['total'] or 0
        
        status_breakdown = {}
        for status_choice, _ in RoundWoodPurchase.STATUS_CHOICES:
            status_breakdown[status_choice] = self.queryset.filter(
                status=status_choice
            ).count()
        
        return Response({
            'total_purchases': total_purchases,
            'total_volume_cubic_feet': float(total_volume),
            'total_spent': float(total_spent),
            'status_breakdown': status_breakdown,
            'pending_purchases': self.queryset.filter(status='pending').count(),
            'completed_purchases': self.queryset.filter(status='completed').count(),
        })


class RoundWoodInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """View current round wood inventory (read-only)"""
    queryset = RoundWoodInventory.objects.all().select_related('wood_type')
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

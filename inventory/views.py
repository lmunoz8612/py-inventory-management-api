from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Inventory, InventoryTransfer
from .serializers import InventorySerializer, InventoryTransferSerializer
from datetime import datetime

class InventoryViewSet(viewsets.ViewSet):
    def list(self, request):
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory, many = True)
        return Response(serializer.data)

    def create(self, request):
        serializer = InventorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class InventoryTransferViewSet(viewsets.ViewSet):
    def list(self, request):
        inventoryTransfer = InventoryTransfer.objects.all()
        serializer = InventoryTransferSerializer(inventoryTransfer, many = True)
        return Response(serializer.data)

    def create(self, request):
        serializer = InventoryTransferSerializer(data = request.data)
        if serializer.is_valid():
            data = serializer.data
            productId = data['productId']
            sourceStoreId = data['sourceStoreId']
            targetStoreId = data['targetStoreId']
            quantity = data['quantity']
            type = data['type']

            sourceStoreInventory = Inventory.objects(productId = productId, storeId = sourceStoreId).first()
            if not sourceStoreInventory or sourceStoreInventory.quantity < quantity:
                return Response({ 'error' : 'Insufficient stock in source store.' }, status = status.HTTP_400_BAD_REQUEST)
            sourceStoreInventory.quantity -= quantity
            sourceStoreInventory.save()

            targetStoreInventory = Inventory.objects(productId = productId, storeId = targetStoreId).first()
            if targetStoreInventory:
                targetStoreInventory.quantity += quantity
            else:
                targetStoreInventory = Inventory(productId = productId, storeId = targetStoreId, quantity = quantity, minStock = quantity)
            targetStoreInventory.save()

            InventoryTransfer(
                productId = productId,
                sourceStoreId = sourceStoreId,
                targetStoreId = targetStoreId,
                quantity = quantity,
                timestamp = datetime.utcnow(),
                type = type
            ).save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class InventoryAlertsViewSet(viewsets.ViewSet):
    def list(self, request):
        inventory_alerts = Inventory.objects.all()
        serializer = InventorySerializer(inventory_alerts, many=True)
        data = serializer.data
        lowStockProducts = [
            item for item in data 
            if isinstance(item.get('quantity'), (int, float)) 
            and isinstance(item.get('minStock'), (int, float)) 
            and item['quantity'] < item['minStock']
        ]
        return Response(lowStockProducts, status=status.HTTP_200_OK)
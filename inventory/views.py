from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Inventory, InventoryTransfer
from .serializers import InventorySerializer, InventoryTransferSerializer
from datetime import datetime


class InventoryViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="List all inventory",
        responses={200: InventorySerializer(many=True)},
    )
    def list(self, request):
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Register a new product to inventory",
        request_body=InventorySerializer,
        responses={201: InventorySerializer(many=True)},
    )
    def create(self, request):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryTransferViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="List inventory transfers",
        responses={200: InventoryTransferSerializer(many=True)},
    )
    def list(self, request):
        inventoryTransfer = InventoryTransfer.objects.all()
        serializer = InventoryTransferSerializer(inventoryTransfer, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Register a new inventory transfer",
        request_body=InventoryTransferSerializer,
        responses={201: InventoryTransferSerializer(many=True)},
    )
    def create(self, request):
        serializer = InventoryTransferSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            productId = data["productId"]
            sourceStoreId = data["sourceStoreId"]
            targetStoreId = data["targetStoreId"]
            quantity = data["quantity"]

            sourceStoreInventory = Inventory.objects.filter(
                productId=productId, storeId=sourceStoreId
            ).first()
            if not sourceStoreInventory or sourceStoreInventory.quantity < quantity:
                return Response(
                    {
                        "detail": "Insufficient stock in source store.",
                        "code": "insufficient_stock",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            sourceStoreInventory.quantity -= quantity
            if sourceStoreInventory.quantity < sourceStoreInventory.minStock:
                return Response(
                    {
                        "detail": f"Required minimum stock in source store is {sourceStoreInventory.minStock}",
                        "code": "minimum_stock_required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            sourceStoreInventory.save()

            targetStoreInventory = Inventory.objects.filter(
                productId=productId, storeId=targetStoreId
            ).first()
            if targetStoreInventory:
                targetStoreInventory.quantity += quantity
            else:
                targetStoreInventory = Inventory(
                    productId=productId,
                    storeId=targetStoreId,
                    quantity=quantity,
                    minStock=quantity,
                )
            targetStoreInventory.save()

            InventoryTransfer(
                productId=productId,
                sourceStoreId=sourceStoreId,
                targetStoreId=targetStoreId,
                quantity=quantity,
                timestamp=datetime.utcnow(),
            ).save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryAlertsViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="List products with low stock",
        responses={200: InventoryTransferSerializer(many=True)},
    )
    def list(self, request):
        inventory_alerts = Inventory.objects.all()
        serializer = InventorySerializer(inventory_alerts, many=True)
        data = serializer.data
        lowStockProducts = [
            item
            for item in data
            if isinstance(item.get("quantity"), (int, float))
            and isinstance(item.get("minStock"), (int, float))
            and item["quantity"] < item["minStock"]
        ]

        return Response(lowStockProducts, status=status.HTTP_200_OK)

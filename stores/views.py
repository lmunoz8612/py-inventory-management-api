from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Store
from .serializers import StoreSerializer

# Inventario
from inventory.models import Inventory
from inventory.serializers import InventorySerializer

class StoreViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary = 'List all stores',
        responses = { 200: StoreSerializer(many = True) }
    )
    def list(self, request):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many = True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary = 'Retrieve store',
        responses = { 200: StoreSerializer(many = True) }
    )
    def retrieve(self, request, pk = None):
        try:
            stores = Store.objects.get(pk = pk)
        except Store.DoesNotExist:
            return Response({'error': 'Store not found.'}, status = status.HTTP_404_NOT_FOUND)
        serializer = StoreSerializer(stores)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary = 'Register a new store',
        request_body = StoreSerializer,
        responses = { 201: StoreSerializer(many = True) }
    )
    def create(self, request):
        serializer = StoreSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary = 'Update an existing store',
        request_body = StoreSerializer,
        responses = { 200: StoreSerializer(many = True) }
    )
    def update(self, request, pk = None):
        try:
            store = Store.objects.get(pk = pk)
        except Store.DoesNotExist:
            return Response({'error': 'Store not found.'}, status = status.HTTP_404_NOT_FOUND)

        serializer = StoreSerializer(store, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class StoreInventoryViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary = 'List inventory by store',
        responses = { 200: InventorySerializer(many = True) }
    )
    def list(self, request, id):
        inventory = Inventory.objects(storeId = id)
        serializer = InventorySerializer(inventory, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Store
from .serializers import StoreSerializer

# Inventario
from inventory.models import Inventory
from inventory.serializers import InventorySerializer

class StoreViewSet(viewsets.ViewSet):
    def list(self, request):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many = True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk = None):
        try:
            stores = Store.objects.get(pk = pk)
        except Store.DoesNotExist:
            return Response({'error': 'Store not found.'}, status = status.HTTP_404_NOT_FOUND)
        serializer = StoreSerializer(stores)
        return Response(serializer.data)

    def create(self, request):
        serializer = StoreSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
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
    def list(self, request, id):
        inventory = Inventory.objects(storeId = id)
        serializer = InventorySerializer(inventory, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


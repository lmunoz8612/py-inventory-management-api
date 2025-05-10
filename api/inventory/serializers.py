from rest_framework import serializers
from .models import Inventory

class InventorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    productId = serializers.CharField(max_length = 25)
    storeId = serializers.CharField(max_length = 25)
    quantity = serializers.IntegerField(min_value = 0, max_value = 99999)
    minStock = serializers.IntegerField(min_value = 0, max_value = 99999)

    def create(self, validated_data):
        inventory = Inventory(**validated_data)
        inventory.save()
        return inventory

class InventoryTransferSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    productId = serializers.CharField(max_length = 25)
    sourceStoreId = serializers.CharField(max_length = 25)
    targetStoreId = serializers.CharField(max_length = 25)
    quantity = serializers.IntegerField(min_value = 0, max_value = 99999)
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", input_formats=["%Y-%m-%dT%H:%M:%S.%fZ"])
    type = serializers.ChoiceField(choices=['IN', 'OUT', 'TRANSFER'])

    def create(self, validated_data):
        inventoryTransfer = InventoryTransfer(**validated_data)
        inventoryTransfer.save()
        return inventoryTransfer

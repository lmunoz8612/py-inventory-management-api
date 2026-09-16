from rest_framework import serializers
from .models import Inventory, InventoryTransfer
from products.models import Product
from stores.models import Store
class InventorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    productId = serializers.CharField(max_length = 25)
    storeId = serializers.CharField(max_length = 25)
    quantity = serializers.IntegerField(min_value = 1, max_value = 99999)
    minStock = serializers.IntegerField(min_value = 1, max_value = 99999)
    def validate_productId(self, value):
        query = Product.objects.filter(id=value)

        # Evalúa si la consulta no devolvió al menos un elemento
        if query.count() == 0:
            raise serializers.ValidationError({
                "detail": "Product with ID {0} does not exist." . format(value),
                "code": "product_not_valid"
            })
        
        return value
    
    def validate_storeId(self, value):
            query = Store.objects.filter(id=value)
    
            # Evalúa si la consulta no devolvió al menos un elemento .exists()
            if query.count() == 0:
                raise serializers.ValidationError({
                    "detail": "Store with ID {0} does not exist." . format(value),
                    "code": "store_not_valid"
                })
            
            return value

    def create(self, validated_data):
        product_id = validated_data.get('productId')
        store_id = validated_data.get('storeId')
        quantity = validated_data.get('quantity')
        min_stock = validated_data.get('minStock')

        # Buscar si ya existe la relación Producto-Almacén
        inventory = Inventory.objects.filter(
            productId=product_id, 
            storeId=store_id
        ).first()

        if inventory:
            # Si ya existe, actualiza los valores (Upsert)
            # Nota: Puedes decidir si sumas la cantidad (+=) o la sobrescribes (=)
            inventory.quantity += quantity  # O inventory.quantity = quantity
            inventory.minStock = min_stock
            inventory.save()
            return inventory
        else:
            # Si no existe, crea el registro nuevo
            inventory = Inventory.objects.create(**validated_data)
            return inventory

class InventoryTransferSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    productId = serializers.CharField(max_length = 25)
    sourceStoreId = serializers.CharField(max_length = 25)
    targetStoreId = serializers.CharField(max_length = 25)
    quantity = serializers.IntegerField(min_value = 1, max_value = 99999)
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", input_formats=["%Y-%m-%dT%H:%M:%S"])

    def validate_productId(self, value):
        query = Product.objects.filter(id=value)

        # Evalúa si la consulta no devolvió al menos un elemento .exists()
        if query.count() == 0:
            raise serializers.ValidationError({
                "detail": "Product with ID {0} does not exist." . format(value),
                "code": "product_not_valid"
            })
        
        return value
    
    def validate_sourceStoreId(self, value):
            query = Store.objects.filter(id=value)
    
            # Evalúa si la consulta no devolvió al menos un elemento .exists()
            if query.count() == 0:
                raise serializers.ValidationError({
                    "detail": "Source Store with ID {0} does not exist." . format(value),
                    "code": "source_store_not_valid"
                })
            
            return value

    def validate_targetStoreId(self, value):
            query = Store.objects.filter(id=value)
    
            # Evalúa si la consulta no devolvió al menos un elemento .exists()
            if query.count() == 0:
                raise serializers.ValidationError({
                    "detail": "Target Store with ID {0} does not exist." . format(value),
                    "code": "target_store_not_valid"
                })
            
            return value

    def create(self, validated_data):
        inventoryTransfer = InventoryTransfer(**validated_data)
        inventoryTransfer.save()
        return inventoryTransfer

from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    name = serializers.CharField(max_length = 100)
    description = serializers.CharField(max_length = 255)
    category = serializers.CharField(max_length = 100)
    price = serializers.FloatField()
    sku = serializers.CharField(max_length = 50)
    def validate_sku(self, value):
        query = Product.objects.filter(sku=value)

        # Si es actualización, excluye el objeto actual
        if self.instance:
            query = query.filter(id__ne=self.instance.id)

        # Evalúa si la consulta devolvió al menos un elemento
        if query.count() > 0:
            raise serializers.ValidationError({
                "detail": "A product with this SKU already exists.",
                "code": "sku_already_exists"
            })
        
        return value

    def create(self, validated_data):
        product = Product(**validated_data)
        product.save()
        return product

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

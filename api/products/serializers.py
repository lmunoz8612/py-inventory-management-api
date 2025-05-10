from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    name = serializers.CharField(max_length = 100)
    description = serializers.CharField(max_length = 255)
    category = serializers.CharField(max_length = 100)
    price = serializers.FloatField()
    sku = serializers.CharField(max_length = 50)

    def create(self, validated_data):
        product = Product(**validated_data)
        product.save()
        return product

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

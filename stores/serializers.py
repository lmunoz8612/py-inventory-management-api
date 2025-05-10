from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    name = serializers.CharField(max_length = 100)
    description = serializers.CharField(max_length = 255)

    def create(self, validated_data):
        store = Store(**validated_data)
        store.save()
        return store

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

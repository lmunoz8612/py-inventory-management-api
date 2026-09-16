from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    name = serializers.CharField(max_length = 100)
    description = serializers.CharField(max_length = 255)

    def validate_name(self, value):
        query = Store.objects.filter(name=value)

        # Si es actualización, excluye el objeto actual
        if self.instance:
            query = query.filter(id__ne=self.instance.id)

        # Evalúa si la consulta devolvió al menos un elemento
        if query.count() > 0:
            raise serializers.ValidationError({
                "detail": "A store with this name already exists.",
                "code": "store_name_already_exists"
            })
        
        return value

    def create(self, validated_data):
        store = Store(**validated_data)
        store.save()
        return store

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

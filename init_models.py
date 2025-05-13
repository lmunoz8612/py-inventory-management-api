from mongoengine import Document, StringField, FloatField, IntField, DateTimeField
from datetime import datetime

class Product(Document):
    name = StringField(required = True, max_length = 100)
    description = StringField('', max_length = 255)
    category = StringField(required = True, max_length = 100)
    price = FloatField(required = True)
    sku = StringField(required = True, max_length = 50)
    meta = {
        'collection': 'products',
        'indexes': [
            'name',
            'sku'
        ]
    }

class Store(Document):
    name = StringField(required = True, max_length = 100)
    description = StringField('', max_length = 255)
    meta = {
        'collection': 'stores',
        'indexes': [
            'name'
        ]
    }

class Inventory(Document):
    productId = StringField(required = True, max_length = 25)
    storeId = StringField(required = True, max_length = 25)
    quantity = IntField(required = True)
    minStock = IntField()
    meta = {
        'collection': 'inventory',
        'indexes': [
            'productId',
            'storeId'
        ]
    }

class InventoryTransfer(Document):
    productId = StringField(required = True, max_length = 25)
    sourceStoreId = StringField(required = True, max_length = 25)
    targetStoreId = StringField(required = True, max_length = 25)
    quantity = IntField(required = True)
    timestamp = timestamp = DateTimeField(required=True, default=datetime.utcnow)
    type = StringField(required = True, max_length = 50, choices = ['IN', 'OUT', 'TRANSFER'])
    meta = {
        'collection': 'inventory_transfers',
        'indexes': [
            'productId',
            'sourceStoreId',
            'targetStoreId',
        ]
    }

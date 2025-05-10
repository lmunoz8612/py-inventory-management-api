from mongoengine import Document, StringField, FloatField, IntField, DateTimeField
from datetime import datetime

class Inventory(Document):
    productId = StringField(required = True, max_length = 25)
    storeId = StringField(required = True, max_length = 25)
    quantity = IntField(required = True)
    minStock = IntField()
    meta = {
        'collection': 'inventory',
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
    }

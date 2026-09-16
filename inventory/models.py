from mongoengine import Document, StringField, IntField, DateTimeField
from datetime import datetime


class Inventory(Document):
    productId = StringField(required=True, max_length=25)
    storeId = StringField(required=True, max_length=25)
    quantity = IntField(required=True)
    minStock = IntField()
    meta = {
        "collection": "inventory",
        "indexes": [{"fields": ["productId", "storeId"], "unique": True}],
    }


class InventoryTransfer(Document):
    productId = StringField(required=True, max_length=25)
    sourceStoreId = StringField(required=True, max_length=25)
    targetStoreId = StringField(required=True, max_length=25)
    quantity = IntField(required=True)
    timestamp = timestamp = DateTimeField(required=True, default=datetime.utcnow)
    meta = {
        "collection": "inventory_transfers",
    }

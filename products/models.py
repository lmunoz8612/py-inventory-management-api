from mongoengine import Document, StringField, FloatField, IntField

class Product(Document):
    name = StringField(required = True, max_length = 100)
    description = StringField('', max_length = 255)
    category = StringField(required = True, max_length = 100)
    price = FloatField(required = True)
    sku = StringField(required = True, max_length = 50)
    meta = {
        'collection': 'products',
    }

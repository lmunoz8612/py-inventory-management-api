from mongoengine import Document, StringField, FloatField, IntField

class Store(Document):
    name = StringField(required = True, max_length = 100)
    description = StringField('', max_length = 255)
    meta = {
        'collection': 'stores',
    }


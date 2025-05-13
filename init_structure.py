from mongoengine import connect
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Conexión a MongoDB
connect(
    db = os.getenv("MONGO_DBNAME"),
    host = os.getenv("MONGO_DBHOST")
)

from init_models import Product, Store, Inventory, InventoryTransfer

Product.drop_collection()
Store.drop_collection()
Inventory.drop_collection()
InventoryTransfer.drop_collection()

# Crear índices explícitamente
Product.ensure_indexes()
Store.ensure_indexes()
Inventory.ensure_indexes()
InventoryTransfer.ensure_indexes()

print("Estructura, datos base e índices creados correctamente.")
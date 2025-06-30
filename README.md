# API de Gestión de Inventario

Esta es una API REST construida con **Django REST Framework** y **MongoDB** (vía `mongoengine`) para administrar productos, inventario por tienda y transferencias entre almacenes.

---

## Instrucciones de instalación

### Requisitos previos

- Python 3.11+
- MongoDB (local o remoto)
- `pip` para gestionar paquetes

### 1. Clonar el repositorio

```bash
git clone https://github.com/lmunoz8612/py-inventory-management-api.git
cd py-inventory-management-api
```

### 2. Endpoints principales:
Método	Endpoint	                Descripción
GET	    /api/inventory/	            Listar inventario
POST	  /api/inventory/	            Registrar nuevo inventario
GET	    /api/inventory-transfers/	  Listar transferencias
POST	  /api/inventory-transfers/	  Registrar transferencia entre almacenes
GET	    /api/inventory-alerts/	    Ver productos con stock bajo

Documentación completa:
- http://[host]:8000/docs/
- http://[host]:8000/docs.json/

### 3. Desiciones técnicas
Base de datos: Se utilizó MongoDB por su flexibilidad de esquema y velocidad en operaciones con documentos.
ODM: Se usó mongoengine para definir modelos de datos de forma declarativa y legible.
Framework: Django REST Framework facilita la creación de APIs robustas con validación, serialización y documentación automática.
Swagger (drf_yasg): Para exponer documentación dinámica de los endpoints.
Estructura modular: Se organizaron las apps por contexto (products, inventory, stores), facilitando el mantenimiento.

### 4. Despliegue en AWS
Ver: AWS_DEPLOYMENT_README.md

### 5. Pruebas
Ver: postman/postman_collection.json

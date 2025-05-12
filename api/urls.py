from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title = 'API Documentation',
        default_version = 'v1',
        description = 'Sistema de Gestión de Inventario',
        terms_of_service = 'https://www.google.com/policies/terms/',
        contact = openapi.Contact(email = 'lvmunozf@outlook.com'),
        license = openapi.License(name = 'BSD License'),
    ),
    public = True,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/stores/', include('stores.urls')),
    path('docs.<format>/', schema_view.without_ui(cache_timeout = 0), name = 'schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout = 0), name = 'schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout = 0), name = 'schema-redoc'),
]
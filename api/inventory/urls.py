from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, InventoryTransferViewSet, InventoryAlertsViewSet

router = DefaultRouter()
router.register(r'inventory', InventoryViewSet, basename = 'inventory')
router.register(r'inventory/transfer', InventoryTransferViewSet, basename = 'inventory-transfer')
router.register(r'inventory/alerts', InventoryAlertsViewSet, basename = 'inventory-alerts')

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, StoreInventoryViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet, basename = 'stores')
store_inventory = StoreInventoryViewSet.as_view({ 'get' : 'list' })

urlpatterns = [
    path('', include(router.urls)),
    path('stores/<str:id>/inventory/', store_inventory, name = 'store-inventory'),
]

from rest_framework import routers
from .api import CarViewSet, ModelnameViewSet, BrandnameViewSet, CarImageViewSet

router = routers.DefaultRouter()
router.register('api/cars', CarViewSet, 'cars')
router.register('api/brandnames', BrandnameViewSet, 'brandnames')
router.register('api/modelnames', ModelnameViewSet, 'modelnames')
router.register('api/carimages', CarImageViewSet, 'carimages')
urlpatterns = router.urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdvertisementViewSet
# Crear el enrutador y registrar el PaymentViewSet
router = DefaultRouter()
#router.register(r'payments', PaymentViewSet)
router.register(r'advertisements', AdvertisementViewSet)


# Definir las URLs
urlpatterns = [
    # Otras URLs...
    path('', include(router.urls)),  # Incluye las URLs del enrutador
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, generate_pdf

# Crear el enrutador y registrar el PaymentViewSet
router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

# Definir las URLs
urlpatterns = [
    # Otras URLs...
    path('', include(router.urls)),  # Incluye las URLs del enrutador
    path('generate-pdf/<int:id>/', generate_pdf, name='generate_pdf'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, SubmissionViewSet, ContentViewSet
# Crear el enrutador y registrar el PaymentViewSet
router = DefaultRouter()
#router.register(r'payments', PaymentViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'contents', ContentViewSet)

# Definir las URLs
urlpatterns = [
    # Otras URLs...
    path('', include(router.urls)),  # Incluye las URLs del enrutador
]

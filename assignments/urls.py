from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, SubmissionViewSet, ContentViewSet, GroupSummaryView, generate_pdf_grades
# Crear el enrutador y registrar el PaymentViewSet
router = DefaultRouter()
#router.register(r'payments', PaymentViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'contents', ContentViewSet)

# Definir las URLs
urlpatterns = [
    # Otras URLs...
    path('group-summary/<int:group_id>/', GroupSummaryView.as_view(), name='group-summary'),
    path('group-summary/<int:id>/generate-pdf/', generate_pdf_grades, name='generate_pdf'),
    path('', include(router.urls)),  # Incluye las URLs del enrutador
]

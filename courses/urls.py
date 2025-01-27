from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, GroupViewSet, ModuleViewSet, EnrollmentViewSet, ModulesByGroupView, generate_pdf,generate_xlsx

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'modules', ModuleViewSet, basename='modules')
router.register(r'enrollments', EnrollmentViewSet, basename='enrrollments')
urlpatterns = [
    path('', include(router.urls)),
    path('group-pdf/<int:id>/', generate_pdf, name='group_pdf'),
    path('group-xlsx/<int:id>/', generate_xlsx, name='group_xlsx'),
    path('groups/<int:group_id>/modules/', ModulesByGroupView.as_view(), name='modules_by_group'),
]
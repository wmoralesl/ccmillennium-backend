from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf.urls.static import static
from django.conf import settings


# Creamos un router para manejar las rutas automáticamente con los ViewSets
router = DefaultRouter()
router.register(r'studentparents', views.StudentParentViewSet, basename='studentParents')
router.register(r'parents', views.ParentViewSet, basename='parents')
router.register(r'users', views.UserViewSet, basename='users')  # Agregamos el ViewSet de usuarios

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user/', views.UserView.as_view(), name='user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),  # Incluimos todas las rutas generadas por el router
]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PredictionViewSet, download_accepted_images

router = DefaultRouter()
router.register(r'predictions', PredictionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('download-accepted-images/', download_accepted_images, name='download_accepted_images'),
]

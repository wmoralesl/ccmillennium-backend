from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import AdvertisementSerializer
from rest_framework import viewsets
from .models import Advertisements
# Create your views here.
class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisements.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']
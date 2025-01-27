from django.shortcuts import render
from rest_framework import viewsets
from .models import Assignment, Submission, Content
from .serializers import AssignmentSerializer, SubmissionSerializer, ContentSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']
    
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']
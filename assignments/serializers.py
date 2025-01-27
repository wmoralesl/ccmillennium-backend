from rest_framework import serializers
from .models import Assignment, Submission, Content

class AssignmentSerializer(serializers.ModelSerializer):
    module_name = serializers.CharField(source='module.name',  read_only=True)
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'created_at', 'file', 'module', 'group', 'module_name', 'due_date', 'grade']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    module_name = serializers.CharField(source='module.name',  read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'description', 'created_at', 'file', 'module', 'group', 'module_name']

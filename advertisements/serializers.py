from rest_framework import serializers
from .models import Advertisements

class AdvertisementSerializer(serializers.ModelSerializer):
    teacher_name  = serializers.CharField(source='teacher.get_full_name',  read_only=True)
    teacher_photo= serializers.ImageField(source='teacher.photo',  read_only=True)
    class Meta:
        model = Advertisements
        fields = ['id', 'description', 'created_at', 'teacher', 'group', 'teacher_name', 'teacher_photo']
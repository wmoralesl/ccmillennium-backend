from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'class_name', 'prediction_value', 'image', 'created_at', 'is_acepted']

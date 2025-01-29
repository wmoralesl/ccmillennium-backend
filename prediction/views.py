from rest_framework import viewsets
from .models import Prediction
from .serializers import PredictionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.conf import settings  # Asegúrate de importar settings
import zipfile
import os
from django.http import HttpResponse

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_reviewed']

def download_accepted_images(request):
    # Filtrar predicciones aceptadas y revisadas
    accepted_images = Prediction.objects.filter(is_acepted=True, is_reviewed=True)

    # Crear un objeto HttpResponse con tipo de contenido ZIP
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=imagenes_aceptadas.zip'

    # Crear un archivo ZIP en memoria
    with zipfile.ZipFile(response, 'w') as zip_file:
        for prediction in accepted_images:
            if prediction.image:
                # Agregar cada imagen al archivo ZIP
                image_path = os.path.join(settings.MEDIA_ROOT, prediction.image.name)
                zip_file.write(image_path, os.path.basename(image_path))

    return response
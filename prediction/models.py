from django.db import models

class Prediction(models.Model):
    class_name = models.CharField(max_length=255)  # Nombre de la clase
    prediction_value = models.FloatField()          # Valor de la predicción
    image = models.ImageField(upload_to='predictions/', blank=True, null=True)  # Imagen opcional
    is_acepted = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return self.class_name

from django.db import models
from django.conf import settings
from datetime import date, timedelta
from courses.models import Group


class Payment(models.Model):
    enrollment = models.ForeignKey('courses.Enrollment', on_delete=models.CASCADE)  # Relaciona con la inscripción
    payment_date = models.DateTimeField(auto_now_add=True)  # Fecha en la que se realiza el pago
    month_paid = models.PositiveIntegerField()  # Indica el mes del curso que se paga
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto del pago
    description = models.TextField(null=True, blank=True)  # Campo para añadir notas o descripciones adicionales
    
    def __str__(self):
        return f"Payment for {self.enrollment.student.email} - Month {self.month_paid} - {self.amount}"

    class Meta:
        unique_together = ('enrollment', 'month_paid')  # Garantiza que solo haya un pago por mes por inscripción


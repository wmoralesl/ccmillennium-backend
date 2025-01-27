from django.db import models
from django.conf import settings
import os
# Create your models here.

class Course(models.Model):
    photo = models.ImageField(upload_to='courses', null=True, blank=True)
    name = models.CharField(max_length=255)
    
    # Tarifas y pagos
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Tarifa mensual del curso.")
    total_payments = models.PositiveIntegerField(null=True, blank=True, help_text="Número total de pagos mensuales.")
    enrollment_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Tarifa única de inscripción.")
    
    # Estado y visibilidad
    is_visible = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        # Elimina el archivo de imagen cuando se elimina la instancia de User
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        self.is_active = False
        self.save()
        
    def group_count(self):
        return self.group_set.count()
    
    
class Module(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    
    def __str__(self):
        return f'{self.name} - {self.course.name}'
    

class Group(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'teacher'},
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    year = models.PositiveIntegerField()
    in_person = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    schedule = models.TimeField()  # Start time of the group
    hours_count = models.PositiveIntegerField()
    is_visible = models.BooleanField(default=True)
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.year})'

    def duration(self):
        return (self.end_date - self.start_date).days

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ['start_date']  # Orders by start date


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'student'}
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, default="Asignación a Curso")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.student.email} - {self.group.name} - {self.enrollment_date}"

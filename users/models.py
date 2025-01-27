from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import os

from .until import user_directory_path, generate_unique_username, validate_image

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Estudiante'),
        ('teacher', 'Maestro'),
        ('admin', 'Administrador'),
    )
    GENDER_CHOICES = (
        ('none', 'No especifica'),
        ('male', 'Hombre'),
        ('female', 'Mujer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    second_last_name = models.CharField(max_length=255, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    dpi = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to=user_directory_path, null=True, blank=True, validators=[validate_image])  # Aquí se agrega el campo de imagen
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='none')
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'second_last_name', 'role']

    def save(self, *args, **kwargs):
        # Obtener la instancia anterior antes de guardar
        try:
            old_user = User.objects.get(pk=self.pk)
        except User.DoesNotExist:
            old_user = None

        # Si hay una imagen nueva o la imagen ha sido eliminada
        if old_user and old_user.photo and old_user.photo != self.photo:
            if os.path.isfile(old_user.photo.path):
                os.remove(old_user.photo.path)

        if not self.username:
            self.username = generate_unique_username(self)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Elimina el archivo de imagen cuando se elimina la instancia de User
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        self.is_active = False
        self.save()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name} {self.second_last_name}'


    def __str__(self):
        return f'**** {self.username} ***** {self.id} - {self.first_name} {self.last_name} {self.second_last_name}'


class Parent(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

class StudentParent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_parents')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.id} - {self.user.first_name} - {self.parent.name if self.parent else "No Parent"}'
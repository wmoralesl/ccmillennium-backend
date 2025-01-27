from django.db import models
from django.conf import settings
from courses.models import Group

# Create your models here.

class Advertisements(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'teacher'},
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.description}'

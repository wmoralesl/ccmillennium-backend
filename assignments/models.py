from django.db import models
from django.conf import settings
from courses.models import Group, Module
from django.utils import timezone

# Función personalizada para generar la ruta de los archivos de las entregas
def submission_directory_path(instance, filename):
    # Obtener el nombre del curso, grupo y el estudiante
    course_name = instance.assignment.group.course.name.replace(" ", "_")  # Reemplazar espacios por guiones bajos
    group_name = instance.assignment.group.name.replace(" ", "_")
    student = instance.student.email  # Usar el correo del estudiante para identificarlo
    # Crear la ruta dinámica
    return f'submissions/{course_name}/{group_name}/{student}/{filename}'

# Función personalizada para generar la ruta del archivo
def assignment_directory_path(instance, filename):
    # Obtener el nombre del curso y grupo
    course_name = instance.group.course.name.replace(" ", "_")  # Reemplazar espacios con guiones bajos
    group_name = instance.group.name.replace(" ", "_")
    # Devolver la ruta dinámica
    return f'submissions/{course_name}/{group_name}/assignments/{filename}'



# Modelo base con los campos comunes
class AssignmentBase(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # La asignación está asociada a un grupo
    file = models.FileField(upload_to=assignment_directory_path, blank=True, null=True)  # Ruta dinámica personalizada

    class Meta:
        abstract = True  # Este modelo es abstracto, no creará una tabla en la base de datos

    def __str__(self):
        return f'{self.title} - Grupo: {self.group.name}'

# Modelo para Tareas (extiende de AssignmentBase)
class Assignment(AssignmentBase):
    due_date = models.DateTimeField()  # Fecha de vencimiento solo para las tareas
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Nota solo para las tareas

    def __str__(self):
        return f'Tarea: {self.title} - Grupo: {self.group.name}'

# Modelo para Contenidos (extiende de AssignmentBase)
class Content(AssignmentBase):
    pass  # Aquí puedes agregar campos específicos al contenido si es necesario en el futuro



# Modelo para las entregas de tareas por los estudiantes
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'student'},
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to=submission_directory_path)  # Ruta dinámica personalizada
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded = models.BooleanField(default=False)  # Indicador de si fue calificado
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Calificación
    feedback = models.TextField(null=True, blank=True)  # Comentarios del maestro

    def __str__(self):
        return f'Entrega de {self.student.email} para {self.assignment.title}'

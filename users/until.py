import os
from django.utils import timezone
from uuid import uuid4
from django.utils.timezone import now
from django.core.exceptions import ValidationError

def user_directory_path(instance, filename):
    """
    Genera una ruta de archivo única para las fotos de usuario.
    """
    # Extraer la extensión del archivo original
    ext = filename.split('.')[-1]
    # Generar un nombre único usando UUID4 y la fecha y hora actual
    unique_filename = "{}_{}.{}".format(uuid4().hex, timezone.now().strftime("%Y%m%d%H%M%S"), ext)
    return os.path.join('photos', unique_filename)

def generate_unique_username(instance):
    """
    Genera un nombre de usuario único basado en el nombre, apellido y año actual.
    """
    base_username = (
        instance.first_name[0].lower() + 
        instance.last_name.lower() + 
        (instance.second_last_name[0].lower() if instance.second_last_name else '') +
        str(now().year)[-2:]
    )
    username = base_username
    counter = 1

    while instance.__class__.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    return username

def validate_image(image):
    file_size = image.size
    limit_kb = 500
    if file_size > limit_kb * 1024:
        raise ValidationError("El tamaño máximo del archivo es %sKB" % limit_kb)
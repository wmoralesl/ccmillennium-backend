from rest_framework import serializers
from .models import User, StudentParent, Parent
from .until import generate_unique_username

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['is_staff', 'is_superuser', 'groups', 'user_permissions']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def create(self, validated_data):
        # Crear la instancia del modelo User con los datos validados
        instance = self.Meta.model(**validated_data)

        # Generar un nombre de usuario único si no se ha proporcionado
        if not instance.username:  # Usa la instancia, no el diccionario
            instance.username = generate_unique_username(instance)

        # Extraer la contraseña y manejarla si se proporciona
        password = validated_data.pop('password', None)  # No lanzará un error si 'password' no está en validated_data

        # Si hay una contraseña proporcionada, establecerla
        if password:
            instance.set_password(password)
        else:
            # Si no se proporciona contraseña, podrías optar por no hacer nada, o establecer un valor por defecto.
            instance.set_password(instance.username)  # Opcional: Asigna el username como contraseña

        # Guardar la instancia
        instance.save()
        return instance
    
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'name', 'phone', 'active']

class StudentParentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Anida el serializador de usuario
    parent = ParentSerializer()  # Ya anidado para mostrar detalles del padre
    
    class Meta:
        model = StudentParent
        fields = ['id', 'user', 'parent']

    def create(self, validated_data):
        parent_data = validated_data.pop('parent')
        parent, created = Parent.objects.get_or_create(**parent_data)
        student_parent = StudentParent.objects.create(parent=parent, **validated_data)
        return student_parent

    def update(self, instance, validated_data):
        parent_data = validated_data.pop('parent')
        parent, created = Parent.objects.get_or_create(**parent_data)
        instance.parent = parent
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
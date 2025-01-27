from rest_framework import serializers
from .models import User, StudentParent, Parent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['is_staff', 'is_superuser', 'groups', 'user_permissions']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
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
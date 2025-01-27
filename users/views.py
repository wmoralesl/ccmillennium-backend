from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from .serializers import UserSerializer, StudentParentSerializer, ParentSerializer
from .models import User, StudentParent, Parent
import jwt, datetime

class RegisterView(APIView):
    def post(self, request):
        # Combinar request.data con request.FILES para crear un diccionario con todos los datos
        data = request.data.copy()
        data.update(request.FILES)

        # Pasar el diccionario combinado al serializador
        serializer = UserSerializer(data=data)
        
        # Validar y guardar
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Devolver los errores del serializador para depurar
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para manejar el login
class LoginView(APIView):
    def post(self, request):
        # email = request.data['email']
        username = request.data['username']
        password = request.data['password']

        # user = User.objects.filter(email=email).first()
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token)

        response.data = {'jwt': token}
        return response

# Vista para obtener y actualizar el usuario autenticado
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Vista para cerrar sesión
class LogoutView(APIView):
    def post(self, request):
        response = Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        response.delete_cookie('jwt')  
        return response 

# Vista para manejar CRUD completo de usuarios usando ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    lookup_field = 'id'
    # permissions_class = [permissions.IsAuthenticated]  # Agrega permisos si es necesario

# Vista para manejar StudentParent
class StudentParentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentParentSerializer

    def get_queryset(self):
        return StudentParent.objects.filter(user__is_active=True, parent__active=True)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response({"message": "Perfil desactivado"}, status=status.HTTP_204_NO_CONTENT)

# Vista para manejar Parent
class ParentViewSet(viewsets.ModelViewSet):
    serializer_class = ParentSerializer

    def get_queryset(self):
        return Parent.objects.filter(active=True)

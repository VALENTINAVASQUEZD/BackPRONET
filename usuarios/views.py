from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import LoginSerializer, RegistroUsuarioSerializer, UsuarioSerializer 
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import PerfilUsuario
from .authentication import UserIDAuthentication


class RegistroUsuarioAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "mensaje": "Usuario registrado exitosamente",
                "id": user.id,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                perfil = user.perfilusuario
                return Response({
                    "mensaje": "Login exitoso",
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "nombre": perfil.nombre,
                    "apellido": perfil.apellido,
                    "fecha_nacimiento": perfil.fecha_nacimiento
                })
            return Response(
                {"error": "Credenciales inválidas"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListarUsuariosAPIView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request, *args, **kwargs):
        usuarios = User.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PerfilUsuarioAPIView(APIView):
    
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
            serializer = UsuarioSerializer(request.user)
            return Response(serializer.data)
        except PerfilUsuario.DoesNotExist:
            return Response(
                {"error": "Perfil no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request):
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
            serializer = EditarPerfilSerializer(perfil, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "mensaje": "Información actualizada exitosamente",
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email,
                    **serializer.data
                })
            return Response({
                "mensaje": "No se pudo actualizar la información. Por favor, verifica los datos ingresados",
                "errores": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except PerfilUsuario.DoesNotExist:
            return Response(
                {"error": "Perfil no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
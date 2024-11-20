from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistroUsuarioSerializer, LoginSerializer, UsuarioSerializer, EditarPerfilSerializer, InformacionAcademicaSerializer, InformacionLaboralSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import PerfilUsuario, InformacionLaboral, InformacionAcademica
from rest_framework.permissions import AllowAny

class RegistroUsuarioAPIView(APIView):
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
    def get(self, request, *args, **kwargs):
        usuarios = User.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PerfilUsuarioAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id=None):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user.is_anonymous:
                return Response({"error": "Se requiere ID de usuario"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            perfil = PerfilUsuario.objects.get(user=user)
            serializer = UsuarioSerializer(user)
            return Response(serializer.data)
        except PerfilUsuario.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id=None):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            if user.is_anonymous:
                return Response({"error": "Se requiere ID de usuario"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            perfil = PerfilUsuario.objects.get(user=user)
            serializer = EditarPerfilSerializer(perfil, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "mensaje": "Información actualizada exitosamente",
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    **serializer.data
                })
            return Response({
                "mensaje": "No se pudo actualizar la información. Por favor, verifica los datos ingresados",
                "errores": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except PerfilUsuario.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
class InformacionAcademicaAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({"error": "Se requiere autenticación"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            info_academica = InformacionAcademica.objects.filter(user=user)
            if not info_academica.exists():
                return Response({"error": "Información académica no encontrada"}, status=status.HTTP_404_NOT_FOUND)

            serializer = InformacionAcademicaSerializer(info_academica, many=True)
            return Response(serializer.data)
        except InformacionAcademica.DoesNotExist:
            return Response({"error": "No hay información académica disponible"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({"error": "Se requiere autenticación"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            info_academica = InformacionAcademica.objects.create(user=user, **request.data)
            serializer = InformacionAcademicaSerializer(info_academica)

            return Response({
                "mensaje": "Información académica creada exitosamente",
                **serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class InformacionLaboralAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({"error": "Se requiere autenticación"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            info_laboral = InformacionLaboral.objects.filter(user=user)
            if not info_laboral.exists():
                return Response({"error": "Información laboral no encontrada"}, status=status.HTTP_404_NOT_FOUND)

            serializer = InformacionLaboralSerializer(info_laboral, many=True)
            return Response(serializer.data)
        except InformacionLaboral.DoesNotExist:
            return Response({"error": "No hay información laboral disponible"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({"error": "Se requiere autenticación"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            info_laboral = InformacionLaboral.objects.create(user=user, **request.data)
            serializer = InformacionLaboralSerializer(info_laboral)

            return Response({
                "mensaje": "Información laboral creada exitosamente",
                **serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PerfilUsuario
from .serializer import RegistroUsuarioSerializer, LoginUsuarioSerializer
from django.contrib.auth.hashers import make_password

class RegistroUsuarioAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contraseña=make_password(serializer.validated_data['contraseña']))
            return Response({'mensaje': 'Usuario registrado exitosamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        lista_usuarios = PerfilUsuario.objects.all()
        serializer = RegistroUsuarioSerializer(lista_usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class LoginUsuarioAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'mensaje': 'Inicio de sesión exitoso'}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
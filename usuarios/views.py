from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from .models import PerfilUsuario
from .serializer import RegistroUsuarioSerializer, LoginUsuarioSerializer

class RegistroUsuarioAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response(
                {'mensaje': 'Usuario registrado exitosamente'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUsuarioAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            correo = serializer.validated_data['correo']
            contraseña = serializer.validated_data['contraseña']
            
            try:
                usuario = PerfilUsuario.objects.get(correo=correo)
                if usuario.check_password(contraseña):
                    
                    return Response(
                        {'mensaje': 'Inicio de sesión exitoso'},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'mensaje': 'Credenciales inválidas'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except PerfilUsuario.DoesNotExist:
                return Response(
                    {'mensaje': 'Credenciales inválidas'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
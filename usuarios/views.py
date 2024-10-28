from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PerfilUsuario
from .serializer import RegistroUsuarioSerializer

class RegistroUsuarioAPIView(APIView):
    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response(
                {'mensaje': 'Usuario registrado exitosamente'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

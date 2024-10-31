from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import EditarPerfilSerializer
from usuarios.models import PerfilUsuario
from usuarios.authentication import UserIDAuthentication

class EditarPerfilAPIView(APIView):
    authentication_classes = [UserIDAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
            serializer = EditarPerfilSerializer(perfil)
            return Response({
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                **serializer.data
            })
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
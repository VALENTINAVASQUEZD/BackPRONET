from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EditarPerfilSerializer
from usuarios.models import PerfilUsuario
from django.contrib.auth.models import User

class EditarPerfilAPIView(APIView):
    def get(self, request, user_id=None):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                perfil = PerfilUsuario.objects.get(user=user)
            except (User.DoesNotExist, PerfilUsuario.DoesNotExist):
                return Response(
                    {"error": "Perfil no encontrado"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            perfil = PerfilUsuario.objects.get(user=request.user)

        serializer = EditarPerfilSerializer(perfil)
        return Response({
            "id": perfil.user.id,
            "username": perfil.user.username,
            "email": perfil.user.email,
            **serializer.data
        })

    def put(self, request, user_id=None):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                perfil = PerfilUsuario.objects.get(user=user)
            except (User.DoesNotExist, PerfilUsuario.DoesNotExist):
                return Response(
                    {"error": "Perfil no encontrado"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            perfil = PerfilUsuario.objects.get(user=request.user)

        serializer = EditarPerfilSerializer(perfil, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "mensaje": "Información actualizada exitosamente",
                "id": perfil.user.id,
                "username": perfil.user.username,
                "email": perfil.user.email,
                **serializer.data
            })
        return Response({
            "mensaje": "No se pudo actualizar la información. Por favor, verifica los datos ingresados",
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
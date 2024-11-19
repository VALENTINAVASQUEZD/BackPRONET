from rest_framework import generics, status
from rest_framework.response import Response
from .models import Publicacion
from .serializers import PublicacionSerializer

class ListarCrearPublicacionesView(generics.ListCreateAPIView):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer

    def perform_create(self, serializer):
        usuario_id = self.request.data.get('usuario_id')
        if usuario_id:
            serializer.save(usuario_id=usuario_id)
        else:
            return Response({"error": "Se requiere el ID del usuario"}, status=status.HTTP_400_BAD_REQUEST)
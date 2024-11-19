from rest_framework import serializers
from .models import Publicacion
from usuarios.serializers import UsuarioSerializer

class PublicacionSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Publicacion
        fields = ['id', 'usuario', 'contenido', 'fecha_creacion']
        read_only_fields = ['fecha_creacion']

    def create(self, validated_data):
        usuario = validated_data.pop('usuario', None)
        return Publicacion.objects.create(usuario=usuario, **validated_data)
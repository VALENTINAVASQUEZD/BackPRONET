from rest_framework import serializers
from .models import PerfilUsuario

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = ['username', 'correo', 'contraseña']
        extra_kwargs = {'contraseña': {'write_only': True}}


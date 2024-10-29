from rest_framework import serializers
from .models import PerfilUsuario

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = ['username', 'correo', 'contraseña']
        extra_kwargs = {'contraseña': {'write_only': True}}
        
class LoginUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = ['correo', 'contraseña']
        extra_kwargs = {'contraseña': {'write_only': True}}


from rest_framework import serializers
from .models import PerfilUsuario

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = ['id', 'username', 'correo', 'contraseña']
        extra_kwargs = {'contraseña': {'write_only': True}}
        
class LoginUsuarioSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    contraseña = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            usuario = PerfilUsuario.objects.get(correo=data['correo'])
        except PerfilUsuario.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas.")
        if not usuario.check_password(data['contraseña']):
            raise serializers.ValidationError("Credenciales inválidas.")
        return data

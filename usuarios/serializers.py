from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PerfilUsuario


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    fecha_nacimiento = serializers.DateField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'nombre', 'apellido', 'fecha_nacimiento']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        nombre = validated_data.pop('nombre')
        apellido = validated_data.pop('apellido')
        fecha_nacimiento = validated_data.pop('fecha_nacimiento')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        PerfilUsuario.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento
        )

        return user


#listar usarios 

class UsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='perfilusuario.nombre')
    apellido = serializers.CharField(source='perfilusuario.apellido')
    fecha_nacimiento = serializers.CharField(source='perfilusuario.fecha_nacimiento')

    class Meta:
        model = User
        fields = ['username', 'email', 'nombre', 'apellido', 'fecha_nacimiento']

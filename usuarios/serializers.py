from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PerfilUsuario, InformacionAcademica, InformacionLaboral
from datetime import date
from django.core.exceptions import ValidationError


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    fecha_nacimiento = serializers.DateField()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'nombre', 'apellido', 'fecha_nacimiento']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_fecha_nacimiento(self, value):
        hoy = date.today()
        edad = hoy.year - value.year - ((hoy.month, hoy.day) < (value.month, value.day))
        if edad < 13:
            raise serializers.ValidationError("El usuario debe tener al menos 13 años de edad.")
        return value

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

class UsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='perfilusuario.nombre')
    apellido = serializers.CharField(source='perfilusuario.apellido')
    fecha_nacimiento = serializers.DateField(source='perfilusuario.fecha_nacimiento')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nombre', 'apellido', 'fecha_nacimiento']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class EditarPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = ['nombre', 'apellido', 'fecha_nacimiento']

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value

    def validate_apellido(self, value):
        if not value.strip():
            raise serializers.ValidationError("El apellido no puede estar vacío")
        return value

    def validate_fecha_nacimiento(self, value):
        from .models import validar_edad_minima
        try:
            validar_edad_minima(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.apellido = validated_data.get('apellido', instance.apellido)
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.save()
        return instance


class InformacionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacionAcademica
        fields = ['id', 'user', 'institucion', 'carrera', 'especialidades']
        read_only_fields = ['id', 'user']

    def validate_institucion(self, value):
        if not value.strip():
            raise serializers.ValidationError("La institución no puede estar vacía.")
        return value

    def validate_carrera(self, value):
        if not value.strip():
            raise serializers.ValidationError("La carrera no puede estar vacía.")
        return value

class InformacionLaboralSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacionLaboral
        fields = ['id', 'user', 'empresa', 'puesto', 'descripcion', 'horas_trabajadas']
        read_only_fields = ['id', 'user']

    def validate_empresa(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre de la empresa no puede estar vacío.")
        return value

    def validate_puesto(self, value):
        if not value.strip():
            raise serializers.ValidationError("El puesto no puede estar vacío.")
        return value

    def validate_horas_trabajadas(self, value):
        if value < 0:
            raise serializers.ValidationError("Las horas trabajadas no pueden ser negativas.")
        return value
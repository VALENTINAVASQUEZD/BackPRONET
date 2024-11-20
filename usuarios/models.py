from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

def validar_edad_minima(fecha_nacimiento):
    if isinstance(fecha_nacimiento, str):
        return
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    if edad < 13:
        raise ValidationError('El usuario debe tener al menos 13 años de edad.')

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(validators=[validar_edad_minima])

    def __str__(self):
        return f'{self.user.username} - Perfil'

class InformacionAcademica(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institucion = models.CharField(max_length=255)
    carrera = models.CharField(max_length=255)
    especialidades = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.carrera}'

class InformacionLaboral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=255)
    puesto = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    horas_trabajadas = models.PositiveIntegerField(default=0)  # Nuevo campo

    def __str__(self):
        return f'{self.user.username} - {self.puesto}'

from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

def validar_edad_minima(fecha_nacimiento):
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    if edad < 13:
        raise ValidationError('El usuario debe tener al menos 13 años de edad.')
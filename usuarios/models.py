from django.db import models

class PerfilUsuario(models.Model):
    correo = models.EmailField(max_length=100, unique=True)
    contraseña = models.CharField(max_length=128)
    username = models.CharField(max_length=150, unique=True, default='usuario_inactivo')


from django.db import models
from django.contrib.auth.hashers import check_password

class PerfilUsuario(models.Model):
    correo = models.EmailField(max_length=100, unique=True)
    contraseña = models.CharField(max_length=128)
    username = models.CharField(max_length=150, unique=True, default='usuario_inactivo')

    def check_password(self, raw_password):
            return check_password(raw_password, self.contraseña)
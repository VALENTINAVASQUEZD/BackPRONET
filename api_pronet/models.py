from django.db import models

class Publicacion(models.Model):
    
    titulo=models.CharField(max_length=50)
    contenido=models.TextField()
    fecha_creacion=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


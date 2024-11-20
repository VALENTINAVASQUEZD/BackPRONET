from django.urls import path
from .views import ListarCrearPublicacionesView

urlpatterns = [
    path('', ListarCrearPublicacionesView.as_view(), name='listar_crear_publicaciones'),
]
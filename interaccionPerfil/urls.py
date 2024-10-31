from django.urls import path
from .views import EditarPerfilAPIView

urlpatterns = [
    path('editar/', EditarPerfilAPIView.as_view(), name='editar_perfil'),
]
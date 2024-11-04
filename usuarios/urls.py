from django.urls import path
from .views import ListarUsuariosAPIView

urlpatterns = [

    path('listar/', ListarUsuariosAPIView.as_view(), name='listar_usuarios'),
]
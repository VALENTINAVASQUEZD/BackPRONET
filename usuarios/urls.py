from django.urls import path
from .views import ListarUsuariosAPIView, RegistroUsuarioAPIView

urlpatterns = [
    path('registro/', RegistroUsuarioAPIView.as_view(), name='registro_usuario'), 
    path('listar/', ListarUsuariosAPIView.as_view(), name='listar_usuarios'),   

]
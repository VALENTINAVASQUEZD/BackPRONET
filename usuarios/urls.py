from django.urls import path
from .views import RegistroUsuarioAPIView,LoginAPIView, PerfilUsuarioAPIView

urlpatterns = [
    path('registro/', RegistroUsuarioAPIView.as_view(), name='registro_usuario'),
    path('login/', LoginAPIView.as_view(), name='login_usuario'),
    path('perfil/', PerfilUsuarioAPIView.as_view(), name='perfil_usuario'),
]

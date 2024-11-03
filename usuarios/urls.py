from django.urls import path
from .views import LoginAPIView, PerfilUsuarioAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login_usuario'),
    path('perfil/', PerfilUsuarioAPIView.as_view(), name='perfil_usuario'),
]

from django.urls import path
from .views import RegistroUsuarioAPIView
from .views import LoginUsuarioAPIView

urlpatterns = [
    path('registro', RegistroUsuarioAPIView.as_view(), name='registro-usuario'),
    path('login', LoginUsuarioAPIView.as_view, name='login-usuario'),
    
]

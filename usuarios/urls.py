from django.urls import path
from .views import RegistroUsuarioAPIView
from .views import LoginUsuarioAPIView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('registro', RegistroUsuarioAPIView.as_view(), name='registro-usuario'),
    path('login', csrf_exempt(LoginUsuarioAPIView.as_view), name='login-usuario'),
    
]

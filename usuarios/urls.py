from django.urls import path
from .views import (RegistroUsuarioAPIView,LoginAPIView,PerfilUsuarioAPIView,ListarUsuariosAPIView,InformacionAcademicaAPIView,InformacionLaboralAPIView,DetalleInformacionAcademicaAPIView,DetalleInformacionLaboralAPIView)

urlpatterns = [
    path('registro/', RegistroUsuarioAPIView.as_view(), name='registro_usuario'),
    path('login/', LoginAPIView.as_view(), name='login_usuario'),
    path('perfil/', PerfilUsuarioAPIView.as_view(), name='perfil_usuario'),
    path('listar/', ListarUsuariosAPIView.as_view(), name='listar_usuarios'),
    path('informacion-academica/', InformacionAcademicaAPIView.as_view(), name='informacion_academica'),
    path('informacion-academica/<int:pk>/', DetalleInformacionAcademicaAPIView.as_view(), name='detalle_informacion_academica'),
    path('informacion-laboral/', InformacionLaboralAPIView.as_view(), name='informacion_laboral'),
    path('informacion-laboral/<int:pk>/', DetalleInformacionLaboralAPIView.as_view(), name='detalle_informacion_laboral'),
]

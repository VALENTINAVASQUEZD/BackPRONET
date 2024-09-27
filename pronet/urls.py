"""
URL configuration for pronet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import UserPublicacionAPIView  # Asegúrate de tener la ruta correcta a tu vista

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para acceder al admin de Django
    path('user/<int:user_id>/publicaciones/', UserPublicacionAPIView.as_view(), name='user-publicaciones'),  # Ruta para ver publicaciones de un usuario
]

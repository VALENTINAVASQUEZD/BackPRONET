from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import  EditarPerfilSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import PerfilUsuario



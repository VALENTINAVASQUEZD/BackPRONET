from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegistroUsuarioSerializer, UsuarioSerializer

class RegistroUsuarioAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #listar usuarios
class ListarUsuariosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        usuarios = User.objects.all()  
        serializer = UsuarioSerializer(usuarios, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)

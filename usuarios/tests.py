from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import PerfilUsuario,InformacionAcademica, InformacionLaboral
from datetime import date
from .serializers import InformacionAcademicaSerializer, InformacionLaboralSerializer


class UsuariosTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpass123',
            'nombre': 'Test',
            'apellido': 'User',
            'fecha_nacimiento': '2000-01-01'
        }
        
        self.user = User.objects.create_user(
            username='existinguser',
            password='12345',
            email='existing@test.com'
        )
        self.perfil = PerfilUsuario.objects.create(
            user=self.user,
            nombre='Existing',
            apellido='User',
            fecha_nacimiento=date(2000, 1, 1)
        )

    def test_registro_usuario(self):
        response = self.client.post('/api/usuarios/registro/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(PerfilUsuario.objects.filter(user__username='testuser').exists())

    def test_registro_usuario_invalido(self):
        data = self.user_data.copy()
        data['fecha_nacimiento'] = '2020-01-01'
        response = self.client.post('/api/usuarios/registro/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_usuario(self):
        response = self.client.post('/api/usuarios/login/', {
            'username': 'existinguser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')
        self.assertEqual(response.data['nombre'], 'Existing')

    def test_login_invalido(self):
        response = self.client.post('/api/usuarios/login/', {
            'username': 'existinguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listar_usuarios(self):
        response = self.client.get('/api/usuarios/listar/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_perfil_usuario(self):
       # self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/usuarios/perfil/12')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')
        self.assertEqual(response.data['nombre'], 'Existing')



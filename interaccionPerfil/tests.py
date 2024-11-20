from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from usuarios.models import PerfilUsuario
from datetime import date

class InteraccionPerfilTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            email='test@test.com'
        )
        self.perfil = PerfilUsuario.objects.create(
            user=self.user,
            nombre='Test',
            apellido='User',
            fecha_nacimiento=date(2000, 1, 1)
        )
        self.client.force_authenticate(user=self.user)
        
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='12345',
            email='test2@test.com'
        )
        self.perfil2 = PerfilUsuario.objects.create(
            user=self.user2,
            nombre='Test2',
            apellido='User2',
            fecha_nacimiento=date(2000, 1, 1)
        )

    def test_get_perfil_propio(self):
        response = self.client.get(f'/api/usuarios/perfil/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Test')
        self.assertEqual(response.data['apellido'], 'User')

    def test_get_perfil_otro_usuario(self):
        response = self.client.get(f'/api/usuarios/perfil/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Test2')
        self.assertEqual(response.data['apellido'], 'User2')

    def test_editar_perfil_valido(self):
        data = {
            'nombre': 'Updated',
            'apellido': 'Name',
            'fecha_nacimiento': '2000-01-01'
        }
        response = self.client.put(f'/api/usuarios/perfil/{self.user.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Updated')
        self.assertEqual(response.data['apellido'], 'Name')

    def test_editar_perfil_invalido(self):
        data = {
            'nombre': '',
            'apellido': '',
            'fecha_nacimiento': '2020-01-01'
        }
        response = self.client.put(f'/api/usuarios/perfil/{self.user.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_perfil_no_encontrado(self):
        response = self.client.get('/api/usuarios/perfil/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Publicacion
from datetime import datetime

class PublicacionesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            email='test@test.com'
        )
        
        self.publicacion = Publicacion.objects.create(
            usuario=self.user,
            contenido='Test content'
        )

    def test_listar_publicaciones(self):
        response = self.client.get('/api/publicaciones/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_crear_publicacion_sin_autenticar(self):
        data = {'contenido': 'New content', 'usuario_id': self.user.id}
        response = self.client.post('/api/publicaciones/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_publicacion_autenticado(self):
        self.client.force_authenticate(user=self.user)
        data = {'contenido': 'New content', 'usuario_id': self.user.id}
        response = self.client.post('/api/publicaciones/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contenido'], 'New content')
        self.assertEqual(response.data['usuario']['username'], 'testuser')

    def test_modelo_publicacion(self):
        publicacion = Publicacion.objects.get(id=self.publicacion.id)
        self.assertEqual(publicacion.contenido, 'Test content')
        self.assertEqual(publicacion.usuario, self.user)
        self.assertTrue(isinstance(publicacion.fecha_creacion, datetime))

    def test_ordenamiento_publicaciones(self):
        self.client.force_authenticate(user=self.user)
        data = {'contenido': 'Newer content', 'usuario_id': self.user.id}
        response = self.client.post('/api/publicaciones/', data)
        
        response = self.client.get('/api/publicaciones/')
        self.assertEqual(response.data[0]['contenido'], 'Newer content')
        self.assertEqual(response.data[1]['contenido'], 'Test content')
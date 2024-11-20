
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import PerfilUsuario, InformacionAcademica, InformacionLaboral
from datetime import date

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
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/usuarios/perfil/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')
        self.assertEqual(response.data['nombre'], 'Existing')



class InformacionAcademicaTests(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123"
        )
        # Autenticar al cliente con el usuario de prueba
        self.client.login(username="testuser", password="testpass123")

        # Crear un registro de información académica para el usuario
        self.info_academica = InformacionAcademica.objects.create(
            user=self.user,
            institucion="Test University",
            carrera="Computer Science",
            especialidades="Artificial Intelligence"
        )

    def test_get_informacion_academica(self):
        """
        Prueba para verificar la obtención de la información académica.
        """
        response = self.client.get("/api/usuarios/informacion-academica/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["institucion"], "Test University")
        self.assertEqual(response.data[0]["carrera"], "Computer Science")

    def test_post_informacion_academica(self):
        """
        Prueba para crear nueva información académica.
        """
        data = {
            "institucion": "New University",
            "carrera": "Mathematics",
            "especialidades": "Statistics"
        }
        response = self.client.post("/api/usuarios/informacion-academica/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["institucion"], "New University")
        self.assertEqual(response.data["carrera"], "Mathematics")

    def test_post_informacion_academica_invalida(self):
        """
        Prueba para creación con datos inválidos.
        """
        data = {"institucion": "", "carrera": "", "especialidades": ""}
        response = self.client.post("/api/usuarios/informacion-academica/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("institucion", response.data)
        self.assertIn("carrera", response.data)

    def test_put_informacion_academica(self):
        """
        Prueba para actualizar información académica existente.
        """
        data = {
            "institucion": "Updated University",
            "carrera": "Physics",
            "especialidades": "Astrophysics"
        }
        response = self.client.put(f"/api/usuarios/informacion-academica/{self.info_academica.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["institucion"], "Updated University")
        self.assertEqual(response.data["carrera"], "Physics")

    def test_put_informacion_academica_invalida(self):
        """
        Prueba para actualizar con datos inválidos.
        """
        data = {"institucion": "", "carrera": ""}
        response = self.client.put(f"/api/usuarios/informacion-academica/{self.info_academica.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("institucion", response.data)
        self.assertIn("carrera", response.data)

    def test_delete_informacion_academica(self):
        """
        Prueba para eliminar un registro de información académica.
        """
        response = self.client.delete(f"/api/usuarios/informacion-academica/{self.info_academica.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InformacionAcademica.objects.filter(id=self.info_academica.id).exists())

    def test_delete_informacion_academica_inexistente(self):
        """
        Prueba para eliminar un registro que no existe.
        """
        response = self.client.delete("/api/usuarios/informacion-academica/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
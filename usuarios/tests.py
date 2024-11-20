import pytest
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


@pytest.fixture
def user(db):
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def info_academica(user):
    return InformacionAcademica.objects.create(
        user=user, institucion="Test University", carrera="Engineering", especialidades="AI"
    )

def test_get_informacion_academica(client, user, info_academica):
    client.force_authenticate(user=user)
    response = client.get("/api/usuarios/informacion-academica/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["institucion"] == "Test University"

def test_post_informacion_academica(client, user):
    client.force_authenticate(user=user)
    data = {"institucion": "New University", "carrera": "Mathematics", "especialidades": "Statistics"}
    response = client.post("/api/usuarios/informacion-academica/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["institucion"] == "New University"

def test_put_informacion_academica(client, user, info_academica):
    client.force_authenticate(user=user)
    data = {"institucion": "Updated University", "carrera": "Physics", "especialidades": "Astrophysics"}
    response = client.put(f"/api/usuarios/informacion-academica/{info_academica.id}/", data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["institucion"] == "Updated University"

def test_delete_informacion_academica(client, user, info_academica):
    client.force_authenticate(user=user)
    response = client.delete(f"/api/usuarios/informacion-academica/{info_academica.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert InformacionAcademica.objects.filter(id=info_academica.id).count() == 0


@pytest.fixture
def info_laboral(user):
    return InformacionLaboral.objects.create(
        user=user, empresa="TechCorp", puesto="Developer", descripcion="Backend developer", horas_trabajadas=40
    )

def test_get_informacion_laboral(client, user, info_laboral):
    client.force_authenticate(user=user)
    response = client.get("/api/usuarios/informacion-laboral/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["empresa"] == "TechCorp"

def test_post_informacion_laboral(client, user):
    client.force_authenticate(user=user)
    data = {
        "empresa": "NewCorp",
        "puesto": "Analyst",
        "descripcion": "Data analyst",
        "horas_trabajadas": 35,
    }
    response = client.post("/api/usuarios/informacion-laboral/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["empresa"] == "NewCorp"

def test_put_informacion_laboral(client, user, info_laboral):
    client.force_authenticate(user=user)
    data = {
        "empresa": "UpdatedCorp",
        "puesto": "Senior Developer",
        "descripcion": "Lead developer",
        "horas_trabajadas": 45,
    }
    response = client.put(f"/api/usuarios/informacion-laboral/{info_laboral.id}/", data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["empresa"] == "UpdatedCorp"

def test_delete_informacion_laboral(client, user, info_laboral):
    client.force_authenticate(user=user)
    response = client.delete(f"/api/usuarios/informacion-laboral/{info_laboral.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert InformacionLaboral.objects.filter(id=info_laboral.id).count() == 0

    
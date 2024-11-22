from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import PerfilUsuario,InformacionAcademica, InformacionLaboral
from datetime import date
from .serializers import InformacionAcademicaSerializer, InformacionLaboralSerializer
from rest_framework.exceptions import ValidationError



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

class InformacionAcademicaSerializerTests(TestCase):

    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_validate_institucion_success(self):
        data = {'institucion': 'Universidad Nacional'}
        serializer = InformacionAcademicaSerializer(data=data)
        self.assertEqual(serializer.validate_institucion(data['institucion']), 'Universidad Nacional')

    def test_validate_institucion_empty(self):
        data = {'institucion': '   '}
        serializer = InformacionAcademicaSerializer()
        with self.assertRaises(ValidationError) as context:
            serializer.validate_institucion(data['institucion'])
        self.assertEqual(str(context.exception.detail[0]), "La institución no puede estar vacía.")

    def test_validate_carrera_success(self):
        data = {'carrera': 'Ingeniería de Sistemas'}
        serializer = InformacionAcademicaSerializer(data=data)
        self.assertEqual(serializer.validate_carrera(data['carrera']), 'Ingeniería de Sistemas')

    def test_validate_carrera_empty(self):
        data = {'carrera': '   '}
        serializer = InformacionAcademicaSerializer()
        with self.assertRaises(ValidationError) as context:
            serializer.validate_carrera(data['carrera'])
        self.assertEqual(str(context.exception.detail[0]), "La carrera no puede estar vacía.")

    def test_validate_especialidades_success(self):
        data = {'especialidades': 'Ciberseguridad'}
        serializer = InformacionAcademicaSerializer(data=data)
        self.assertEqual(serializer.validate_especialidades(data['especialidades']), 'Ciberseguridad')

    def test_validate_especialidades_empty(self):
        data = {'especialidades': '   '}
        serializer = InformacionAcademicaSerializer()
        with self.assertRaises(ValidationError) as context:
            serializer.validate_especialidades(data['especialidades'])
        self.assertEqual(str(context.exception.detail[0]), "Las especialidades no pueden estar vacías.")


class InformacionLaboralSerializerTests(TestCase):

    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_validate_empresa_success(self):
        data = {'empresa': 'TechCorp'}
        serializer = InformacionLaboralSerializer(data=data)
        self.assertEqual(serializer.validate_empresa(data['empresa']), 'TechCorp')

    def test_validate_empresa_empty(self):
        data = {'empresa': '   '}
        serializer = InformacionLaboralSerializer()
        with self.assertRaises(ValidationError) as context:
            serializer.validate_empresa(data['empresa'])
        self.assertEqual(str(context.exception.detail[0]), "El nombre de la empresa no puede estar vacío.")

    def test_validate_puesto_success(self):
        data = {'puesto': 'Desarrollador'}
        serializer = InformacionLaboralSerializer(data=data)
        self.assertEqual(serializer.validate_puesto(data['puesto']), 'Desarrollador')

    def test_validate_puesto_empty(self):
        data = {'puesto': '   '}
        serializer = InformacionLaboralSerializer()
        with self.assertRaises(ValidationError) as context:
            serializer.validate_puesto(data['puesto'])
        self.assertEqual(str(context.exception.detail[0]), "El puesto no puede estar vacío.")

    def test_validate_horas_trabajadas_success(self):
        data = {'horas_trabajadas': 40}
        serializer = InformacionLaboralSerializer(data=data)
        self.assertEqual(serializer.validate_horas_trabajadas(data['horas_trabajadas']), 40)

    def test_validate_horas_trabajadas_negative(self):
        data = {'horas_trabajadas': -5}
        serializer = InformacionLaboralSerializer()
        with self.assertRaises(ValidationError) as context:
            serializer.validate_horas_trabajadas(data['horas_trabajadas'])
        self.assertEqual(str(context.exception.detail[0]), "Las horas trabajadas no pueden ser negativas.")


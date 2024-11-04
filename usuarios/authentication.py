from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import User

class UserIDAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user_id = request.META.get('HTTP_X_USER_ID')
        
        if not user_id:
            return None

        try:
            user = User.objects.get(id=user_id)
            return (user, None)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No existe un usuario con ese ID')
        except ValueError:
            raise exceptions.AuthenticationFailed('ID de usuario inválido')
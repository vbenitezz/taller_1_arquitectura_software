from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class Email_Backend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Buscamos al usuario por el email, que se pasa como 'username'
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None

        # Verificamos la contraseña
        if user.check_password(password):
            return user
        return None

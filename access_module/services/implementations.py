from .interfaces import AbstractUserRegistrationService
from django.contrib.auth import authenticate, login
from django.contrib import messages
from ..models import Restaurant_Chain, Foundation

class DjangoUserRegistrationService(AbstractUserRegistrationService):
    def register_user(self, cleaned_data, user_type):
        if user_type == 'restaurant chain':
            user = Restaurant_Chain.objects.create(
                nit=cleaned_data['nit'],
                name=cleaned_data['name'],
                email=cleaned_data['email']
            )
        elif user_type == 'foundation':
            user = Foundation.objects.create(
                nit=cleaned_data['nit'],
                name=cleaned_data['name'],
                email=cleaned_data['email']
            )
        else:
            return None

        user.set_password(cleaned_data['password1'])
        user.save()
        return user

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class Custom_User_Manager(BaseUserManager):
    def create_user(self, email, name, nit, password=None, **extra_fields):
        if not email:
            raise ValueError('The user should have an email')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, nit=nit, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, nit, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, nit, password, **extra_fields)
class Custom_User(AbstractUser):
    username = None
    nit = models.PositiveIntegerField(unique=True) 
    name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    selected_branch = models.ForeignKey('Restaurant_Chain_Branch', null=True, blank=True, on_delete=models.SET_NULL)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['name', 'nit']

    objects = Custom_User_Manager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
    )

class Foundation(Custom_User):
    pass
class Restaurant_Chain(Custom_User):
    pass

class Restaurant_Chain_Branch(models.Model):
    id_restaurant_chain = models.ForeignKey(Restaurant_Chain, on_delete=models.CASCADE, related_name='branches')
    image = models.ImageField(upload_to="restaurant_chain/branch_images/", null=True)
    branch = models.CharField(max_length=60)
    address = models.CharField(max_length=200)


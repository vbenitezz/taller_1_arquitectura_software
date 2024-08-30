from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class User(AbstractUser):
#     nit = models.PositiveIntegerField() 
#     name = models.CharField(max_length=60)
#     # username
#     # email
#     # password
# class Fundation(User):
#     pass
# class Restaurant_Chain(User):
#     pass
# class Restaurant_Chain_Branch(models.Model):
#     id_restaurant_chain = models.ForeignKey(Restaurant_Chain, on_delete=models.CASCADE)
#     branch = models.CharField(max_length=60)
#     address = models.CharField(max_length=200)
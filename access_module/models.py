from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#class Custom_User(AbstractUser):
#    nit = models.PositiveIntegerField() 
#    name = models.CharField(max_length=60)
 #   user_type = models.CharField(max_length=15)
 #   email = models.EmailField()

#class Fundation(Custom_User):
#    pass
#class Restaurant_Chain(Custom_User):
#    pass

#class Restaurant_Chain_Branch(models.Model):
#    id_restaurant_chain = models.ForeignKey(Restaurant_Chain, on_delete=models.CASCADE, #related_name='branches')
#    branch = models.CharField(max_length=60)
#    address = models.CharField(max_length=200) 
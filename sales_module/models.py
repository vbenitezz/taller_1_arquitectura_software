from django.db import models
from inventory_module.models import Published_Product
from access_module.models import Foundation

# Create your models here.

class Publication(models.Model):
    creation_date = models.DateField(auto_now_add=True, unique=True)
    def __str__(self):
        return f'Publication ({self.creation_date})'
class Published_Product_Publication(models.Model):
    id_published_product = models.ForeignKey(Published_Product, on_delete=models.CASCADE)
    id_publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('id_published_product', 'id_publication')

class Order(models.Model):
    customer = models.ForeignKey(Foundation,null=True,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20)
    order_date = models.DateField(auto_now_add=True)
    total_price = models.IntegerField()

class Cart_Product(models.Model):
    cart_product = models.ForeignKey(Published_Product,null=True, on_delete=models.CASCADE)
    order =  models.ForeignKey(Order, on_delete=models.CASCADE,null=True,related_name='products')
    quantity = models.IntegerField(null=True)
from django.db import models
from inventory_module.models import Published_Product

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
class Cart_Product(models.Model):
    id_published_product_publication = models.ForeignKey(Published_Product_Publication, on_delete=models.CASCADE)
    cart_quantity = models.PositiveIntegerField()
    @property
    def name_product(self):
        return self.id_published_product_publication.id_published_product.name_product
    @property
    def image_product(self):
        return self.id_published_product_publication.id_published_product.image_product
    @property
    def publish_price_published_product(self):
        return self.id_published_product_publication.id_published_product.publish_price
    @property
    def total_price_product(self):
        return self.cart_quantity * self.publish_price_published_product
class Shopping_Cart(models.Model):
    total_price = models.PositiveIntegerField()
class Cart_Product_Shopping_Cart(models.Model):
    id_cart_product = models.ForeignKey(Cart_Product, on_delete=models.CASCADE)
    id_shopping_cart = models.ForeignKey(Shopping_Cart, on_delete=models.CASCADE)
    @property
    def total_price_shopping_cart(self):
        return self.id_shopping_cart.total_price
    @property
    def name_product(self):
        return self.id_cart_product.name_product
    @property
    def image_product(self):
        return self.id_cart_product.image_product
    @property
    def publish_price_published_product(self):
        return self.id_cart_product.publish_price_published_product
    @property
    def cart_quantity_cart_product(self):
        return self.id_cart_product.cart_quantity
    @property
    def total_price_product_cart_product(self):
        return self.id_cart_product.total_price_product
class Purchase(models.Model):
    id_cart_product_shopping_cart = models.ForeignKey(Cart_Product_Shopping_Cart, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20)
    purchase_date = models.DateField(auto_now_add=True)
    @property
    def total_price_shopping_cart(self):
        return self.id_cart_product_shopping_cart.total_price_shopping_cart
    @property
    def name_product(self):
        return self.id_cart_product_shopping_cart.name_product
    @property
    def cart_quantity_cart_product(self):
        return self.id_cart_product_shopping_cart.cart_quantity_cart_product
    @property
    def total_price_product_cart_product(self):
        return self.id_cart_product_shopping_cart.total_price_product_cart_product
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_product_cart_product_consumer/<int:id>/', views.get_product_cart_product_consumer),
    path('shopping_cart/', views.show_shopping_cart, name='show_shopping_cart')
]
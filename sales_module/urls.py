from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_products_for_sale, name='view_products_for_sale'),
    path('foundation/', views.view_products_for_donate, name='view_products_for_donate'),
    path('get_product_cart_product_consumer/<int:id>/', views.get_product_cart_product_consumer),
    path('shopping_cart/', views.show_shopping_cart, name='show_shopping_cart')
]
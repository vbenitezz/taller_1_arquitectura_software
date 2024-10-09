from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_products_for_sale, name='view_products_for_sale'),
    path('foundation/', views.view_products_for_donate, name='view_products_for_donate'),
    path('get_product_cart_product_consumer/<int:id>/', views.get_product_cart_product_consumer),
    path('shopping_cart/', views.show_shopping_cart, name='show_shopping_cart'),
    path('shopping_cart_foundation/', views.show_shopping_cart_foundation, name='show_shopping_cart_foundation'),
    path('update_product_quantity/', views.update_product_quantity, name='update_product_quantity'),
    path('buy_order_consumer/', views.buy_order_consumer, name='buy_order_consumer'),
    path('buy_order_foundation/', views.buy_order_foundation, name='buy_order_foundation'),
    path('show_orders/', views.show_orders, name='show_orders')



]
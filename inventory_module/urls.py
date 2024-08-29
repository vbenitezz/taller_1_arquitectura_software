from django.urls import path
from . import views

urlpatterns = [
    path('home_restaurant_chain/', views.home_restaurant_chain, name='home_restaurant_chain'),
    path('inventory/', views.show_product, name='inventory'),
    path('add_product/', views.add_product),
    path('inventory/delete_product/<int:id>/', views.delete_product),
    path('inventory/before_edit_product/<int:id>/', views.before_edit_product),
    path('edit_product/', views.edit_product),
    path('add_publish_product/', views.add_publish_product, name='add_publish_product'),
]
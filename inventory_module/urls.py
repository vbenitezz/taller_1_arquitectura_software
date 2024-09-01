from django.urls import path
from . import views

urlpatterns = [
    path('home_restaurant_chain/', views.home_restaurant_chain, name='home_restaurant_chain'),
    path('inventory/', views.show_product, name='inventory'),
    path('create_product/', views.create_product),
    path('inventory/delete_product/<int:id>/', views.delete_product),
    path('get_product/<int:id>/', views.get_product, name='get_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),

    
    
    path('add_product/', views.a),
    path('search_products_suggestions/', views.search_products_suggestions, name='search_products_suggestions'),
    path('prueba_show/',views.prueba_show,name='prueba_show'),
    path('add_product/',views.add_product)

    # path('add_publish_product/', views.add_publish_product, name='add_publish_product'),
]
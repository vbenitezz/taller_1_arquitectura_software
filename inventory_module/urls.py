from django.urls import path
from . import views

urlpatterns = [
    path('home_restaurant_chain/', views.home_restaurant_chain, name='home_restaurant_chain'),
    path('delete_published_product/<int:id_product>/', views.delete_published_product),

    path('inventory/', views.show_product, name='inventory'),
    path('create_product/', views.create_product),
    path('inventory/delete_product/<int:id>/', views.delete_product),
    path('get_product/<int:id>/', views.get_product, name='get_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),

    # add_product
    path('get_product_add_product/<int:id>/', views.get_product_add_product),
    path('edit_product_add_product/<int:id>/', views.edit_product_add_product),
    path('add_product/delete_product_add_product/<int:id>/', views.delete_product_add_product),


    path('add_product_function/', views.add_product_function),
    path('add_product/', views.add_product_view, name='add_product'),
    path('search_products_suggestions/', views.search_products_suggestions, name='search_products_suggestions'),
    path('show_add_product/',views.show_add_product,name='show_add_product'),

    path('publish_product/',views.publish_product,name='publish_product')

    # path('add_publish_product/', views.add_publish_product, name='add_publish_product'),
]
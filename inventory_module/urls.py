from django.urls import path
from .views import (
    HomeRestaurantChainView, DeletePublishedProductView, 
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    AddProductView, AddProductFunctionView, SearchProductsSuggestionsView, 
    PublishProductView
)

urlpatterns = [
    path('home_restaurant_chain/', HomeRestaurantChainView.as_view(), name='home_restaurant_chain'),
    path('delete_published_product/<int:id_product>/', DeletePublishedProductView.as_view(), name='delete_published_product'),

    path('inventory/', ProductListView.as_view(), name='inventory'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('edit_product/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete_product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),

    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('add_product_function/', AddProductFunctionView.as_view(), name='add_product_function'),

    path('search_products_suggestions/', SearchProductsSuggestionsView.as_view(), name='search_products_suggestions'),
    path('publish_product/', PublishProductView.as_view(), name='publish_product'),
]

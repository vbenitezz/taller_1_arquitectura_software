from django.urls import path
from .views import (
    ViewProductsForSale, ViewProductsForDonate, GetProductCartProductConsumer,
    ShowShoppingCart, ShowShoppingCartFoundation, UpdateProductQuantity,
    UpdateProductDeleteQuantity, BuyOrderConsumer, BuyOrderFoundation,
    ShowOrders, ShowOrderDetail
)

urlpatterns = [
    path('', ViewProductsForSale.as_view(), name='view_products_for_sale'),
    path('foundation/', ViewProductsForDonate.as_view(), name='view_products_for_donate'),
    path('get_product_cart_product_consumer/<int:id>/', GetProductCartProductConsumer.as_view(), name='get_product_cart_product_consumer'),
    path('get_product_cart_product_foundation/<int:id>/', GetProductCartProductConsumer.as_view(), name='get_product_cart_product_foundation'),

    path('shopping_cart/', ShowShoppingCart.as_view(), name='show_shopping_cart'),
    path('shopping_cart_foundation/', ShowShoppingCartFoundation.as_view(), name='show_shopping_cart_foundation'),

    path('update_product_quantity/', UpdateProductQuantity.as_view(), name='update_product_quantity'),
    path('update_product_delete_quantity/', UpdateProductDeleteQuantity.as_view(), name='update_product_delete_quantity'),

    path('buy_order_consumer/', BuyOrderConsumer.as_view(), name='buy_order_consumer'),
    path('buy_order_foundation/', BuyOrderFoundation.as_view(), name='buy_order_foundation'),

    path('show_orders/', ShowOrders.as_view(), name='show_orders'),
    path('show_details/', ShowOrderDetail.as_view(), name='show_details'),
]

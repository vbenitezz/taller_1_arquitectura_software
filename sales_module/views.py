from django.shortcuts import render
from .models import Published_Product
from django.http import JsonResponse

# Create your views here.

def view_products_for_sale(request):
    products = Published_Product.objects.filter(publish_type="sale")
    return render(request, 'show_published_product_consumer.html',{'products':products})
def view_products_for_donate(request):
    products = Published_Product.objects.filter(publish_type='donation')
    return render(request, 'show_published_product_foundation.html', {'products':products})

def get_product_cart_product_consumer(request, id):
    product = Published_Product.objects.get(id=id)
    print(product.publish_price)
    print(product.image_product())
    data = {
        'image': product.image_product(),
        'price': product.publish_price
    }
    print(data)
    return JsonResponse(data)
def show_shopping_cart(request):
    return render(request, 'show_shopping_cart.html') 


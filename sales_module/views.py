from django.shortcuts import render, redirect
from .models import Published_Product, Order, Cart_Product
from access_module.models import Foundation
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def view_products_for_sale(request):
    products = Published_Product.objects.filter(publish_type="sale")
    return render(request, 'show_published_product_consumer.html',{'products':products})

@login_required
def view_products_for_donate(request):
    user = request.user
    if hasattr(user, 'foundation'):
        products = Published_Product.objects.filter(publish_type='donation')
        return render(request, 'show_published_product_foundation.html', {'products':products})
    else:
        return redirect('inventory')

def get_product_cart_product_consumer(request, id):
    product = Published_Product.objects.get(id=id)
    print(product.publish_price)
    print(product.image_product())
    print(product.name_product)
    print(product.publish_quantity)
    data = {
        'name': product.name_product,
        'image': product.image_product(),
        'price': product.publish_price,
        'publish_quantity': product.publish_quantity
    }
    return JsonResponse(data)
def show_shopping_cart(request):
    return render(request, 'shopping_cart_consumer.html') 

def show_shopping_cart_foundation(request):
    return render(request,'shopping_cart_foundation.html')

@csrf_exempt
def update_product_quantity(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            new_quantity = data.get('quantity')
            print(f"Received quantity: {new_quantity}")

            product = Published_Product.objects.get(id=product_id)
            print(f"Current quantity: {product.publish_quantity}")
            
            product.publish_quantity = new_quantity
            product.save()
            
            updated_product = Published_Product.objects.get(id=product_id)
            print(f"Updated quantity: {updated_product.publish_quantity}")
            
            return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully'})
        except Published_Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def buy_order_consumer(request):
    if request.method == 'POST':
        data =  json.loads(request.body)
        products=json.loads(data['products'])
        order = Order.objects.create(
            payment_method = "cash",
            total_price =  data['total_price']
        )
        for product in products:
            published_product = Published_Product.objects.get(id=int(product['id']))
            Cart_Product.objects.create(
                cart_product=published_product,
                order=order,
                quantity=int(product['quantity'])
                )
        return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully'})
    

@login_required
@csrf_exempt
def buy_order_foundation(request):
    if request.method == 'POST':
        user_email = request.user.email
        user = Foundation.objects.get(email=user_email)
        data =  json.loads(request.body)
        products=json.loads(data['products'])
        order = Order.objects.create(
            customer = user,
            payment_method = "cash",
            total_price =  data['total_price']
        )
        for product in products:
            published_product = Published_Product.objects.get(id=int(product['id']))
            Cart_Product.objects.create(
                cart_product=published_product,
                order=order,
                quantity=int(product['quantity'])
                )
        return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully'})
    
def show_orders(request):
    if request.user.is_authenticated:
        print('AUTENTICADO')
        user=Foundation.objects.get(email=request.user.email)
        orders = Order.objects.filter(customer=user)
        return  render(request, 'show_orders.html', {'orders':orders})
    else:
        
        orders = Order.objects.filter(customer__isnull=True)
        for order in list(orders):
            print(f'PRODUCTOS DE LA ORDEN: {order.id}')
            for product in order.products.all():
                print(f'{product.cart_product.name_product}')
        return  render(request, 'show_orders.html', {'orders':orders})






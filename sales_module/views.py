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
    data = {
        'name': product.name_product,
        'image': product.image_product(),
        'price': product.publish_price,
        'publish_quantity': product.publish_quantity,
        'place': product.place,
        'address': product.pick_up_address

    }
    print(data)
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
            
            print(f"Updated quantity: {product.publish_quantity}")

            return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully'})
        except Published_Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def update_product_delete_quantity(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            new_quantity = data.get('quantity')
            print(f"Received quantity: {new_quantity}")

            product = Published_Product.objects.get(id=product_id)
            print(f"Current quantity: {product.publish_quantity}")
            
            product.publish_quantity += new_quantity
            product.save()
            
            print(f"Updated quantity: {product.publish_quantity}")

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
        print(products)
        order = Order.objects.create(
            payment_method = "cash",
            total_price =  data['total_price']
        )
        for product in products:
            published_product = Published_Product.objects.get(id=int(product['id']))
            image_path = product['image'].replace('/media/', '')
            Cart_Product.objects.create(
                image=image_path,
                name=published_product.name_product,
                price=published_product.publish_price,
                order=order,
                quantity=int(product['quantity'])
                )
            if(published_product.publish_quantity==0):

                published_product.delete()
        return JsonResponse({'status': 'success', 'message': 'Products bought successfully'})
    

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
            image_path = product['image'].replace('/media/', '')
            Cart_Product.objects.create(
                image=image_path,
                name=published_product.name_product,
                price=published_product.publish_price,
                order=order,
                quantity=int(product['quantity']),
                place= published_product.place,
                pick_up_address= published_product.pick_up_address
                )
            if(published_product.publish_quantity==0):
                published_product.delete()
            
        return JsonResponse({'status': 'success', 'message': 'Products bought successfully'})
    
def show_orders(request):
    if request.user.is_authenticated:
        user=Foundation.objects.get(email=request.user.email)
        orders = Order.objects.filter(customer=user)
        return  render(request, 'show_orders.html', {'orders':orders})
    else:
        orders = Order.objects.filter(customer__isnull=True)
        return  render(request, 'show_orders.html', {'orders':orders})
    
def show_order_detail(request):
    if request.method=='POST':
        data = json.loads(request.body)
        order_id=data['order_id']
        order = Order.objects.get(id=order_id)
        products = order.products.all()
        products_data = []
        for product in products:
            products_data.append({
                'id': product.id,
                'image':product.image.url,
                'name': product.name,
                'price': product.price,
                'quantity': product.quantity,
                'place': product.place,
                'address': product.pick_up_address
            })


        return JsonResponse({'products': products_data})
    return JsonResponse({'error':'Unexpected method type'})







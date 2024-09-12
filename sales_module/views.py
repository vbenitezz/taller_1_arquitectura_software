from django.shortcuts import render, redirect
from .models import Published_Product
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
            
            updated_product = Published_Product.objects.get(id=product_id)
            print(f"Updated quantity: {updated_product.publish_quantity}")
            
            return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully'})
        except Published_Product.DoesNotExist:
            print("NO EXISTEEEEEEEEEEEEEEEEEEEEEEEEE")
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


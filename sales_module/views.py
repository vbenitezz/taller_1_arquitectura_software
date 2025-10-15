from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
import json

from .models import Published_Product, Order, Cart_Product
from inventory_module.models import Wasted_Product
from access_module.models import Foundation

class ViewProductsForSale(View):

    def get(self, request):
        products = Published_Product.objects.filter(publish_type="sale")
        current_time = datetime.now().strftime("%H:%M:%S")

        for product in products:
            time_obj = product.pick_up_time.strftime("%H:%M:%S")
            if current_time > time_obj:
                Wasted_Product.objects.create(
                    id_product_inventory=product.id_product_inventory,
                    wasted_quantity=product.publish_quantity
                )
                product.delete()

        return render(request, 'show_published_product_consumer.html', {'products': products})


class ViewProductsForDonate(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        if hasattr(user, 'foundation'):
            products = Published_Product.objects.filter(publish_type="donation")
            current_time = datetime.now().strftime("%H:%M:%S")

            for product in products:
                time_obj = product.pick_up_time.strftime("%H:%M:%S")
                if current_time > time_obj:
                    Wasted_Product.objects.create(
                        id_product_inventory=product.id_product_inventory,
                        wasted_quantity=product.publish_quantity
                    )
                    product.delete()

            return render(request, 'show_published_product_foundation.html', {'products': products})
        return redirect('inventory')

class GetProductCartProductConsumer(View):

    def get(self, request, id):
        product = Published_Product.objects.get(id=id)
        data = {
            'name': product.name_product,
            'image': product.image_product(),
            'price': product.publish_price,
            'publish_quantity': product.publish_quantity,
            'place': product.place,
            'address': product.pick_up_address
        }
        return JsonResponse(data)

class ShowShoppingCart(View):

    def get(self, request):
        return render(request, 'shopping_cart_consumer.html')


class ShowShoppingCartFoundation(View):

    def get(self, request):
        return render(request, 'shopping_cart_foundation.html')

@method_decorator(csrf_exempt, name='dispatch')
class UpdateProductQuantity(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            new_quantity = data.get('quantity')

            product = Published_Product.objects.get(id=product_id)
            product.publish_quantity = new_quantity
            product.save()

            return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully'})
        except Published_Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateProductDeleteQuantity(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            new_quantity = data.get('quantity')

            product = Published_Product.objects.get(id=product_id)
            product.publish_quantity += new_quantity
            product.save()

            return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully'})
        except Published_Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class BuyOrderConsumer(View):

    def post(self, request):
        data = json.loads(request.body)
        products = json.loads(data['products'])
        order = Order.objects.create(
            payment_method="cash",
            total_price=data['total_price']
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
                place=published_product.place,
                pick_up_address=published_product.pick_up_address,
                category=published_product.category_product
            )
            if published_product.publish_quantity == 0:
                published_product.delete()

        return JsonResponse({'status': 'success', 'message': 'Products bought successfully'})

@method_decorator(csrf_exempt, name='dispatch')
class BuyOrderFoundation(LoginRequiredMixin, View):

    def post(self, request):
        user_email = request.user.email
        user = Foundation.objects.get(email=user_email)
        data = json.loads(request.body)
        products = json.loads(data['products'])
        order = Order.objects.create(
            customer=user,
            payment_method="cash",
            total_price=data['total_price']
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
                place=published_product.place,
                pick_up_address=published_product.pick_up_address
            )
            if published_product.publish_quantity == 0:
                published_product.delete()

        return JsonResponse({'status': 'success', 'message': 'Products bought successfully'})


class ShowOrders(View):

    def get(self, request):
        if request.user.is_authenticated:
            user = Foundation.objects.get(email=request.user.email)
            orders = Order.objects.filter(customer=user)
        else:
            orders = Order.objects.filter(customer__isnull=True)
        return render(request, 'show_orders.html', {'orders': orders})

@method_decorator(csrf_exempt, name='dispatch')
class ShowOrderDetail(View):

    def post(self, request):
        data = json.loads(request.body)
        order_id = data['order_id']
        order = Order.objects.get(id=order_id)
        products = order.products.all()

        products_data = [{
            'id': p.id,
            'image': p.image.url,
            'name': p.name,
            'price': p.price,
            'quantity': p.quantity,
            'place': p.place,
            'address': p.pick_up_address
        } for p in products]

        return JsonResponse({'products': products_data})

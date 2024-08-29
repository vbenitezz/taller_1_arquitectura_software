from django.shortcuts import render, HttpResponse, redirect
from .models import Product
from django.contrib import messages

# Create your views here.

def home_restaurant_chain(request):
    return render(request, 'template_inventory.html')
def show_product(request):
    products = Product.objects.all()
    return render(request, 'add_product.html', {'products': products})
def add_product(request):
    name = request.POST['input_name']
    category = request.POST['input_category']
    total_quantity = request.POST['input_total_quantity']
    sale_price = request.POST['input_sale_price']

    product = Product.objects.create(name=name, category=category, total_quantity=total_quantity, sale_price=sale_price)
    return redirect('inventory')
def delete_product(request, id):
    product = Product.objects.get(id=id).delete()
    return redirect('inventory')
def before_edit_product(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'edit_product.html', {'product': product})
def edit_product(request):
    id = request.POST['input_id']
    name = request.POST['input_name']
    category = request.POST['input_category']
    total_quantity = request.POST['input_total_quantity']
    sale_price = request.POST['input_sale_price']

    product = Product.objects.get(id=id)
    product.name = name 
    product.category = category
    product.total_quantity = total_quantity
    product.sale_price = sale_price
    product.save()

    return redirect('inventory')









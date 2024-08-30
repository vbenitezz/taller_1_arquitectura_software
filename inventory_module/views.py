from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages

# Create your views here.

def home_restaurant_chain(request):
    return render(request, 'template_inventory_module.html')
def show_product(request):
    products = Product.objects.all()
    return render(request, 'create_product.html', {'products': products})
def create_product(request):
    name = request.POST['input_name']
    category = request.POST['input_category']
    sale_price = request.POST['input_sale_price']
    description = request.POST['input_description']
    image = request.POST['input_image']
    product = Product.objects.create(name=name, category=category, sale_price=sale_price, description=description, image=image)
    return redirect('inventory')
def delete_product(request, id):
    product = Product.objects.get(id=id).delete()
    return redirect('inventory')
def information_edit_product(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'edit_product.html', {'product': product})
def edit_product(request):
    id = request.POST['input_id']
    name = request.POST['input_name']
    category = request.POST['input_category']
    sale_price = request.POST['input_sale_price']
    description = request.POST['input_description']
    image = request.POST['input_image']

    product = Product.objects.get(id=id)
    product.name = name 
    product.category = category
    product.sale_price = sale_price
    product.description = description
    product.image = image
    product.save()

    return redirect('inventory')









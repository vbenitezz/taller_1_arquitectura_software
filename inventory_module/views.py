from django.shortcuts import render, redirect
from .models import Product,Product_Inventory, Inventory
from django.http import JsonResponse
from django.utils import timezone
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
    image = request.FILES['input_image']
    categories = ['Fast Food', 'Healthy Options', 'Grilled & BBQ', 'Sides', 'Beverages', 'Desserts']
    product = Product.objects.create(name=name, category=categories[int(category)-1], sale_price=sale_price, description=description, image=image)
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

def a(request):
    return render(request,'prueba.html')

def add_product(request):
    name = request.POST['input_name']
    total_quantity = request.POST['input_quantity']
    products = Product.objects.filter(name=name)
    today = timezone.now().date()
    inventories = Inventory.objects.filter(creation_date=today)
    inventory=inventories.first()
    if inventory is None:
        inventory = Inventory.objects.create()

    if products.exists():
        product = products.first()
        product_inventory = Product_Inventory.objects.create(id_product=product,id_inventory=inventory,total_quantity=total_quantity)
    else:
        render(request,'prueba.html',{'products':products});
    
    return redirect('prueba_show')

def prueba_show(request):
    products_inventory = Product_Inventory.objects.all()
    return render(request,'prueba.html',{'products':products_inventory})






def search_products_suggestions(request):
    query = request.GET.get('q','')
    products = Product.objects.filter(name__icontains=query).values('name')
    return JsonResponse(list(products),safe=False)










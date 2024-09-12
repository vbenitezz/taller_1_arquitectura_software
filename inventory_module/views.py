from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Product_Inventory, Inventory, Published_Product
from django.http import JsonResponse
from django.utils import timezone
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def home_restaurant_chain(request):
    return render(request, 'template_inventory_module.html')

@login_required
def show_product(request):
    user = request.user
    if hasattr(user, 'restaurant_chain'):
        products = Product.objects.all()
        return render(request, 'create_product.html', {'products': products})
    else:
        return redirect('view_products_for_donate')
    
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

def get_product(request, id):
    product = Product.objects.get(id=id)
    categories = {'Fast Food': 1, 'Healthy Options': 2, 'Grilled & BBQ': 3, 'Sides': 4, 'Beverages': 5, 'Desserts': 6}
    data = {
        'name': product.name,
        'category': categories[product.category],
        'sale_price': product.sale_price,
        'description': product.description,
        'image': product.image.url if product.image else ''
    }
    print(data)
    return JsonResponse(data)
def edit_product(request, id):
    categories = {1: 'Fast Food', 2: 'Healthy Options', 3: 'Grilled & BBQ', 4: 'Sides', 5: 'Beverages', 6: 'Desserts'}
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        product.name = request.POST.get('name')
        product.category = categories[int(request.POST.get('category'))]
        product.sale_price = request.POST.get('sale_price')
        product.description = request.POST.get('description')
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
    return redirect('inventory')

def get_product_add_product(request, id):
    product_inventory = Product_Inventory.objects.get(id=id)
    data = {
        'name': product_inventory.name_product,
        'quantity': product_inventory.total_quantity
    }
    print(data)
    return JsonResponse(data)

def edit_product_add_product(request, id):
    if request.method == 'POST':
        product_inventory = Product_Inventory.objects.get(id=id)
        product_inventory.total_quantity = request.POST.get('edit_quantity_add_product')
        product_inventory.save()
    return redirect('add_product')
def delete_product_add_product(request, id):
    product_inventory = Product_Inventory.objects.get(id=id).delete()
    return redirect('add_product')


@login_required
def add_product_view(request):
    user = request.user
    if hasattr(user, 'restaurant_chain'):
        products_inventory = Product_Inventory.objects.all()
        return render(request,'add_product.html',{'products':products_inventory})
    else:
        return redirect('view_products_for_donate')

def add_product_function(request):
    name = request.POST['input_name']
    total_quantity = request.POST['input_quantity']
    products = Product.objects.filter(name=name)
    today = timezone.localtime(timezone.now()).date()
    inventory = Inventory.objects.filter(creation_date=today).first()

    if inventory is None:
        inventory = Inventory.objects.create()
    

    if products.exists():
        try:
            product = products.first()
            product_inventory = Product_Inventory.objects.create(
                id_product=product, 
                id_inventory=inventory, 
                total_quantity=total_quantity
            )
            messages.success(request, 'Product added successfully')
        except IntegrityError as e:
            messages.error(request, 'The product you are trying to add has already been added; please delete or edit it')
    else:
        messages.error(request, 'The product you are trying to add is not in the inventory')


    return redirect('show_add_product')

def show_add_product(request):
    products_inventory = Product_Inventory.objects.all()
    return render(request,'add_product.html',{'products':products_inventory})



def search_products_suggestions(request):
    query = request.GET.get('q','')
    products = Product.objects.filter(name__icontains=query).values('name')
    return JsonResponse(list(products),safe=False)

def publish_product(request):
    if request.method == 'POST':
        id_product = int(request.POST['id_product'])
        publish_product_type = request.POST['type']
        published_quantity = int(request.POST['quantity'])
        publish_product_pick_up_time = request.POST['pick_up_time']
        publish_product_price = request.POST['price']

        # Filtrar productos con el mismo ID
        products_with_same_id = Published_Product.objects.filter(id_product_inventory__id_product__id=id_product)

        if products_with_same_id.exists():
            # Si hay productos con el mismo ID, intentar obtener uno con el tipo especificado
            product_with_same_type = products_with_same_id.filter(publish_type=publish_product_type).first()

            if product_with_same_type:
                # Si existe un producto con el mismo ID y tipo, mostrar un mensaje de error
                messages.error(request, 'The product you are trying to publish is already published. If you want to modify it, click here.')
            else:
                # Si no existe un producto con el mismo ID y tipo, crear uno nuevo
                id_published_product = get_object_or_404(Product_Inventory, id_product=id_product)
                id_published_product.total_quantity -= published_quantity
                id_published_product.save()

                published_product = Published_Product.objects.create(
                    id_product_inventory=id_published_product,
                    publish_type=publish_product_type,
                    publish_quantity=published_quantity,
                    publish_price=publish_product_price,
                    pick_up_time=publish_product_pick_up_time
                )
                messages.success(request, 'Product published successfully')
        else:
            # Si no hay productos con el mismo ID, crear uno nuevo
            id_published_product = get_object_or_404(Product_Inventory, id_product=id_product)
            id_published_product.total_quantity -= published_quantity
            id_published_product.save()

            published_product = Published_Product.objects.create(
                id_product_inventory=id_published_product,
                publish_type=publish_product_type,
                publish_quantity=published_quantity,
                publish_price=publish_product_price,
                pick_up_time=publish_product_pick_up_time
            )
            messages.success(request, 'Product published successfully')

        return redirect('add_product')













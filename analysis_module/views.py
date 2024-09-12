from django.shortcuts import render, redirect
from sales_module.models import Published_Product
from django.contrib.auth.decorators import login_required
from inventory_module.models import Product

# Create your views here.
@login_required
def display_graphics(request):
    user = request.user
    if hasattr(user, 'restaurant_chain'):
        products_for_donation = Published_Product.objects.filter(publish_type='donation').count()
        products_for_sale = Published_Product.objects.filter(publish_type='sale').count()
        return render(request, 'index.html', {"products_for_donation":products_for_donation, "products_for_sale":products_for_sale})
    else:
        return redirect('view_products_for_donate')
from django.shortcuts import render
from sales_module.models import Published_Product

# Create your views here.
def display_graphics(request):
    products_for_donation = Published_Product.objects.filter(publish_type='donation').count()
    products_for_sale = Published_Product.objects.filter(publish_type='sale').count()
    return render(request, 'index.html', {"products_for_donation":products_for_donation, "products_for_sale":products_for_sale})
from django.shortcuts import render
from .models import Published_Product

# Create your views here.

def home(request):
    # products = Published_Product.objects.filter(publish_type="sale")
    return render(request, 'template_sales_module.html')

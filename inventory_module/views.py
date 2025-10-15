from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db import IntegrityError

from .models import Product, Product_Inventory, Inventory, Published_Product
from access_module.models import Restaurant_Chain_Branch


# --------------------------------------------------------------
#  CRUD genérico para los productos del inventario
# --------------------------------------------------------------

class ProductListView(LoginRequiredMixin, ListView):
    """Lista todos los productos del restaurante logueado."""
    model = Product
    template_name = 'create_product.html'
    context_object_name = 'products'

    def get_queryset(self):
        user_branch = self.request.user.selected_branch
        return Product.objects.filter(pick_up_address=user_branch.address)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Crea un nuevo producto en el inventario."""
    model = Product
    template_name = 'product_form.html'
    fields = ['name', 'category', 'sale_price', 'description', 'image']

    def form_valid(self, form):
        user_branch = self.request.user.selected_branch
        branch = Restaurant_Chain_Branch.objects.get(id=user_branch.id)
        form.instance.pick_up_address = branch.address
        form.instance.place = branch.branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('inventory')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Edita un producto existente."""
    model = Product
    template_name = 'product_form.html'
    fields = ['name', 'category', 'sale_price', 'description', 'image']

    def get_success_url(self):
        return reverse_lazy('inventory')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina un producto del inventario."""
    model = Product
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('inventory')


# --------------------------------------------------------------
#  Otras vistas complementarias del módulo (no CRUD directo)
# --------------------------------------------------------------

class HomeRestaurantChainView(LoginRequiredMixin, View):
    def get(self, request):
        user_branch_id = request.user.selected_branch.id
        user_branch_address = Restaurant_Chain_Branch.objects.get(id=user_branch_id).address
        products = Published_Product.objects.filter(
            id_product_inventory__id_product__pick_up_address=user_branch_address
        )
        return render(request, 'home_restaurant_chain.html', {'products': products})


class DeletePublishedProductView(View):
    def post(self, request, id_product):
        product = get_object_or_404(Published_Product, id=id_product)
        product.delete()
        return redirect('home_restaurant_chain')


class AddProductView(LoginRequiredMixin, View):
    def get(self, request):
        user_branch_id = request.user.selected_branch.id
        branch = Restaurant_Chain_Branch.objects.get(id=user_branch_id)
        products_inventory = Product_Inventory.objects.filter(
            id_product__pick_up_address=branch.address
        )
        return render(request, 'add_product.html', {'products': products_inventory})


class AddProductFunctionView(View):
    def post(self, request):
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
                Product_Inventory.objects.create(
                    id_product=product,
                    id_inventory=inventory,
                    total_quantity=total_quantity,
                )
                messages.success(request, 'Product added successfully')
            except IntegrityError:
                messages.error(request, 'This product already exists in inventory.')
        else:
            messages.error(request, 'Product not found in inventory.')
        return redirect('show_add_product')


@method_decorator(csrf_exempt, name='dispatch')
class SearchProductsSuggestionsView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        products = Product.objects.filter(name__icontains=query).values('name')
        return JsonResponse(list(products), safe=False)


class PublishProductView(View):
    def post(self, request):
        id_product = int(request.POST['id_product'])
        publish_type = request.POST['type']
        published_quantity = int(request.POST['quantity'])
        price = request.POST.get('price', 0)
        pick_up_time = request.POST['pick_up_time']

        products_with_same_id = Published_Product.objects.filter(
            id_product_inventory__id_product__id=id_product
        )
        id_published_product = get_object_or_404(Product_Inventory, id_product=id_product)

        if products_with_same_id.filter(publish_type=publish_type).exists():
            messages.error(request, 'This product is already published with this type.')
        else:
            id_published_product.total_quantity -= published_quantity
            id_published_product.save()
            Published_Product.objects.create(
                id_product_inventory=id_published_product,
                publish_type=publish_type,
                publish_quantity=published_quantity,
                publish_price=price,
                pick_up_time=pick_up_time,
            )
            messages.success(request, 'Product published successfully')

        return redirect('add_product')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sales_module.models import Published_Product, Order
from inventory_module.models import Product_Inventory
import plotly.graph_objs as go
from collections import defaultdict

CATEGORIES = ['Fast Food', 'Healthy Options', 'Grilled & BBQ', 'Sides', 'Beverages', 'Desserts']

def get_products_sold_data(selected_categories=None):
    data = defaultdict(int)
    orders = Order.objects.exclude(customer_id=None)
    
    for order in orders:
        for product in order.products.all():
            category = product.category
            # Si no hay categorías seleccionadas o la categoría del producto está en las seleccionadas
            if not selected_categories or category in selected_categories:
                data[category] += product.quantity
    
    if not selected_categories:
        return [('Products Sold', sum(data.values()))]
    return [('Products Sold - ' + category, count) for category, count in data.items()]

def get_products_donated_data(selected_categories=None):
    data = defaultdict(int)
    orders = Order.objects.filter(customer_id=None)
    
    for order in orders:
        for product in order.products.all():
            category = product.category
            if not selected_categories or category in selected_categories:
                data[category] += product.quantity
    
    if not selected_categories:
        return [('Products Donated', sum(data.values()))]
    return [('Products Donated - ' + category, count) for category, count in data.items()]

def get_inventory_data(selected_categories=None):
    data = defaultdict(int)
    products = Product_Inventory.objects.all()
    
    for product in products:
        category = product.category
        if not selected_categories or category in selected_categories:
            data[category] += product.total_quantity
    
    if not selected_categories:
        return [('Products in Inventory', sum(data.values()))]
    return [('Inventory - ' + category, count) for category, count in data.items()]

def get_published_data(selected_categories=None):
    data = defaultdict(int)
    products = Published_Product.objects.all()
    
    for product in products:
        category = product.category
        if not selected_categories or category in selected_categories:
            data[category] += product.publish_quantity
    
    if not selected_categories:
        return [('Products Published', sum(data.values()))]
    return [('Published - ' + category, count) for category, count in data.items()]

def get_published_sale_data(selected_categories=None):
    data = defaultdict(int)
    products = Published_Product.objects.filter(publish_type='sale')
    
    for product in products:
        category = product.category
        if not selected_categories or category in selected_categories:
            data[category] += product.publish_quantity
    
    if not selected_categories:
        return [('Products Published for Sale', sum(data.values()))]
    return [('Published Sale - ' + category, count) for category, count in data.items()]

def get_published_donation_data(selected_categories=None):
    data = defaultdict(int)
    products = Published_Product.objects.filter(publish_type='donation')
    
    for product in products:
        category = product.category
        if not selected_categories or category in selected_categories:
            data[category] += product.publish_quantity
    
    if not selected_categories:
        return [('Products Published for Donation', sum(data.values()))]
    return [('Published Donation - ' + category, count) for category, count in data.items()]

@login_required
def display_graphics(request):
    user = request.user
    if hasattr(user, 'restaurant_chain'):
        products_for_donation = Published_Product.objects.filter(publish_type='donation').count()
        products_for_sale = Published_Product.objects.filter(publish_type='sale').count()
        return render(request, 'index.html', {
            "products_for_donation": products_for_donation, 
            "products_for_sale": products_for_sale
        })
    else:
        return redirect('view_products_for_donate')

@login_required
def customize_chart(request):
    user = request.user
    if not hasattr(user, 'restaurant_chain'):
        return redirect('analysis:view_products_for_donate')

    if request.method != 'POST':
        return render(request, 'customize.html', {'is_chart': 0})

    # Procesar la solicitud POST
    chart_type = request.POST.get('chart_type')
    data = []

    # Mapeo de variables a funciones
    variable_functions = {
        '1': get_products_sold_data,
        '2': get_products_donated_data,
        '3': get_inventory_data,
        '4': get_published_data,
        '5': get_published_sale_data,
        '6': get_published_donation_data
    }

    # Procesar cada variable seleccionada
    for var_id in variable_functions.keys():
        if var_id in request.POST.getlist('variables'):
            # Obtener categorías seleccionadas para esta variable
            selected_categories = request.POST.getlist(f'categories{var_id}')
            # Obtener datos usando la función correspondiente
            variable_data = variable_functions[var_id](selected_categories if selected_categories else None)
            data.extend(variable_data)

    if not data:
        return render(request, 'customize.html', {'is_chart': 0})

    # Colores predefinidos
    colors = ['#3C93AF', '#F9AA41', '#4EBC95', '#325F74', '#0E272C', '#FFFFFF']
    
    # Crear el gráfico apropiado
    labels = [item[0] for item in data]
    values = [item[1] for item in data]
    
    if chart_type == '1':  # Pie chart
        chart = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=colors[:len(labels)])
            )],
            layout=go.Layout(
                title='Distribution by Variable and Category',
                height=600
            )
        )
    else:  # Bar chart
        chart = go.Figure(
            data=[go.Bar(
                x=labels,
                y=values,
                marker=dict(color=colors[:len(labels)])
            )],
            layout=go.Layout(
                title='Distribution by Variable and Category',
                xaxis={'title': 'Variables', 'tickangle': 45},
                yaxis={'title': 'Count'},
                height=600
            )
        )

    # Convertir el gráfico a HTML
    chart_html = chart.to_html(full_html=False)

    # Preparar los datos para la tabla de resumen
    summary_data = []
    for label, value in data:
        # Separar el nombre de la variable y la categoría si existe
        if ' - ' in label:
            variable, category = label.split(' - ', 1)
        else:
            variable, category = label, 'All Categories'
        summary_data.append({
            'variable': variable,
            'category': category,
            'value': value
        })

    return render(request, 'customize.html', {
        'is_chart': 1,
        'chart': chart_html,
        'summary_data': summary_data
    })
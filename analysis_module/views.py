from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sales_module.models import Published_Product
from inventory_module.models import Product_Inventory, Published_Product
from sales_module.models import Order
import plotly.graph_objs as go

# Variables predefinidas para las opciones seleccionadas
variables = {
    'products_sold': 0,
    'products_donated': 0,
    'products_in_inventory': 0,
    'products_published': 0,
    'products_published_for_sale': 0,
    'products_published_for_donate': 0
}

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
    if hasattr(user, 'restaurant_chain'):
        if request.method == 'POST':
            chart_type = request.POST.get('chart_type')

            selected_variables = []
            for variable in ['1', '2', '3', '4', '5', '6']:
                if request.POST.get(variable):
                    selected_variables.append(variable)

            data = []
            if '1' in selected_variables:
                data.append(('Products Sold', Order.objects.filter(customer_id=None).count()))
            if '2' in selected_variables:
                data.append(('Products Donated', Order.objects.exclude(customer_id=None).count()))
            if '3' in selected_variables:
                data.append(('Products in Inventory', Product_Inventory.objects.count()))
            if '4' in selected_variables:
                data.append(('Products Published', Published_Product.objects.count()))
            if '5' in selected_variables:
                data.append(('Products Published for Sale', Published_Product.objects.filter(publish_type='sale').count()))
            if '6' in selected_variables:
                data.append(('Products Published for Donation', Published_Product.objects.filter(publish_type='donation').count()))

            if chart_type == '1':  # Pie chart
                labels = [item[0] for item in data]
                values = [item[1] for item in data]
                chart = go.Figure(
                    data=[go.Pie(labels=labels, values=values)],
                    layout=go.Layout(title='Pie Chart: Selected Variables')
                )
            elif chart_type == '2':  # Bar chart
                labels = [item[0] for item in data]
                values = [item[1] for item in data]
                chart = go.Figure(
                    data=[go.Bar(x=labels, y=values)],
                    layout=go.Layout(title='Bar Chart: Selected Variables', xaxis={'title': 'Categories'}, yaxis={'title': 'Count'})
                )

            chart_html = chart.to_html(full_html=False)

            # Retorna tanto el gráfico como los datos en formato tabla
            return render(request, 'customize.html', {
                'is_chart': 1,
                'chart': chart_html,
                'summary_data': data  # Pasamos los datos para la tabla
            })

        return render(request, 'customize.html', {'is_chart': 0})
    else:
        return redirect('analysis:view_products_for_donate')

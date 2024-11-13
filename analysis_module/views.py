from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sales_module.models import Published_Product, Order
from inventory_module.models import Product_Inventory
from inventory_module.models import Wasted_Product
import plotly.graph_objs as go

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
            
            selected_variables = request.POST.getlist('variables')
            categories_variables = {}
            for selected_variable in selected_variables:
                categories_variables[selected_variable] = request.POST.getlist(f'categories{selected_variable}')

            data = []
            if '1' in categories_variables.keys():
                acc_ = 0
                orders = Order.objects.filter(customer_id=None)
                for order in orders:
                    for product in order.products.all():
                        acc_ += product.quantity
                        print(f'{product.id} -> {product.name} : {product.quantity}')
                data.append(('Products Sold', acc_))
                if len(categories_variables['1']) != 0:
                    counter = 0
                    for category in categories_variables['1']:
                        for order in Order.objects.filter(customer_id = None):
                            for product in order.products.all():
                                if product.category == category:
                                    counter = counter + product.quantity
                        data.append((f'Products sold: {category}', counter))
                        counter = 0
            
            if '2' in categories_variables.keys():
                acc_ = 0
                orders = Order.objects.exclude(customer_id=None)
                for order in orders:
                    for product in order.products.all():
                        acc_ += product.quantity
                        print(f'{product.id} -> {product.name} : {product.quantity}')
                data.append(('Products donated', acc_))
                if len(categories_variables['2']) != 0:
                    counter = 0
                    for category in categories_variables['1']:
                        for order in Order.objects.exclude(customer_id = None):
                            for product in order.products.all():
                                if product.category == category:
                                    counter = counter + product.quantity
                        data.append((f'Products sold: {category}', counter))
                        counter = 0
 
            if '3' in categories_variables.keys():
                data.append(('Products in Inventory', sum([product.total_quantity for product in Product_Inventory.objects.all()])))
                if len(categories_variables['3']) != 0:
                    for category in categories_variables['3']:
                        data.append((f'Products in Inventory {category}', sum([product.total_quantity for product in Product_Inventory.objects.filter(id_product__category = category) ])))
                    
            if '4' in categories_variables.keys():
                data.append(('Products Published', sum([product.publish_quantity for product in Published_Product.objects.all()])))
                if len(categories_variables['4']) != 0:
                    for category in categories_variables['4']:
                        data.append((f'Products Published {category}', sum([product.publish_quantity for product in Published_Product.objects.filter(id_product_inventory__id_product__category = category)])))

            if '5' in categories_variables.keys():
                data.append(('Products Published for Sale', sum([product.publish_quantity for product in Published_Product.objects.filter(publish_type='sale')])))
                if len(categories_variables['5']) != 0:
                    for category in categories_variables['5']:
                        data.append((f'Products Published for Sale {category} ', sum([product.publish_quantity for product in Published_Product.objects.filter(publish_type='sale', id_product_inventory__id_product__category = category)])))

            if '6' in categories_variables.keys():
                data.append(('Products Published for donate', sum([product.publish_quantity for product in Published_Product.objects.filter(publish_type='donation')])))
                if len(categories_variables['6']) != 0:
                    for category in categories_variables['6']:
                        data.append((f'Products Published for donate {category} ', sum([product.publish_quantity for product in Published_Product.objects.filter(publish_type='donation', id_product_inventory__id_product__category = category)])))

            if '7' in categories_variables.keys():
                data.append(('Products Wasted', sum([product_wasted.wasted_quantity for product_wasted in Wasted_Product.objects.all()])))
                if len(categories_variables['7']) != 0:
                    for category in categories_variables['7']:
                        data.append((f'Products Wasted {category}', sum([product_wasted.wasted_quantity for product_wasted in Wasted_Product.objects.filter( id_product_inventory__id_product__category=category)])))

            # Colores definidos
            colors = ['#3C93AF', '#F9AA41', '#4EBC95', '#325F74', '#0E272C', '#FFFFFF']

            if chart_type == '1':  # Pie chart
                labels = [item[0] for item in data]
                values = [item[1] for item in data]
                chart = go.Figure(
                    data=[go.Pie(labels=labels, values=values, 
                                  marker=dict(colors=colors[:len(labels)]))],  # Colores según la cantidad de etiquetas
                    layout=go.Layout(title='Pie Chart: Selected Variables')
                )
            elif chart_type == '2':  # Bar chart
                labels = [item[0] for item in data]
                values = [item[1] for item in data]
                chart = go.Figure(
                    data=[go.Bar(x=labels, y=values, 
                                  marker=dict(color=colors[:len(labels)]))],  # Colores según la cantidad de etiquetas
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

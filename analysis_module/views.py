from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from sales_module.models import Published_Product, Order
from inventory_module.models import Product_Inventory, Wasted_Product
import plotly.graph_objs as go

class DisplayGraphicsView(LoginRequiredMixin, View):
    def get(self, request):
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

class CustomizeChartView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        if hasattr(user, 'restaurant_chain'):
            return render(request, 'customize.html', {'is_chart': 0})
        return redirect('analysis:view_products_for_donate')

    def post(self, request):
        user = request.user
        if not hasattr(user, 'restaurant_chain'):
            return redirect('analysis:view_products_for_donate')

        chart_type = request.POST.get('chart_type')
        selected_variables = request.POST.getlist('variables')

        categories_variables = {
            var: request.POST.getlist(f'categories{var}') for var in selected_variables
        }

        data = []

        if '1' in categories_variables.keys():
            acc_ = 0
            orders = Order.objects.filter(customer_id=None)
            for order in orders:
                for product in order.products.all():
                    acc_ += product.quantity
            data.append(('Products Sold', acc_))

            if categories_variables['1']:
                for category in categories_variables['1']:
                    counter = sum(
                        product.quantity
                        for order in Order.objects.filter(customer_id=None)
                        for product in order.products.all()
                        if product.category == category
                    )
                    data.append((f'Products sold: {category}', counter))

        if '2' in categories_variables.keys():
            acc_ = 0
            orders = Order.objects.exclude(customer_id=None)
            for order in orders:
                for product in order.products.all():
                    acc_ += product.quantity
            data.append(('Products donated', acc_))

            if categories_variables['2']:
                for category in categories_variables['2']:
                    counter = sum(
                        product.quantity
                        for order in Order.objects.exclude(customer_id=None)
                        for product in order.products.all()
                        if product.category == category
                    )
                    data.append((f'Products donated: {category}', counter))

        if '3' in categories_variables.keys():
            data.append(('Products in Inventory',
                         sum(product.total_quantity for product in Product_Inventory.objects.all())))

            if categories_variables['3']:
                for category in categories_variables['3']:
                    data.append((
                        f'Products in Inventory {category}',
                        sum(p.total_quantity for p in Product_Inventory.objects.filter(id_product__category=category))
                    ))

        if '4' in categories_variables.keys():
            data.append(('Products Published',
                         sum(p.publish_quantity for p in Published_Product.objects.all())))
            if categories_variables['4']:
                for category in categories_variables['4']:
                    data.append((
                        f'Products Published {category}',
                        sum(p.publish_quantity for p in Published_Product.objects.filter(
                            id_product_inventory__id_product__category=category))
                    ))

        if '5' in categories_variables.keys():
            data.append(('Products Published for Sale',
                         sum(p.publish_quantity for p in Published_Product.objects.filter(publish_type='sale'))))
            if categories_variables['5']:
                for category in categories_variables['5']:
                    data.append((
                        f'Products Published for Sale {category}',
                        sum(p.publish_quantity for p in Published_Product.objects.filter(
                            publish_type='sale',
                            id_product_inventory__id_product__category=category))
                    ))

        if '6' in categories_variables.keys():
            data.append(('Products Published for donate',
                         sum(p.publish_quantity for p in Published_Product.objects.filter(publish_type='donation'))))
            if categories_variables['6']:
                for category in categories_variables['6']:
                    data.append((
                        f'Products Published for donate {category}',
                        sum(p.publish_quantity for p in Published_Product.objects.filter(
                            publish_type='donation',
                            id_product_inventory__id_product__category=category))
                    ))

        if '7' in categories_variables.keys():
            data.append(('Products Wasted',
                         sum(p.wasted_quantity for p in Wasted_Product.objects.all())))
            if categories_variables['7']:
                for category in categories_variables['7']:
                    data.append((
                        f'Products Wasted {category}',
                        sum(p.wasted_quantity for p in Wasted_Product.objects.filter(
                            id_product_inventory__id_product__category=category))
                    ))

        colors = ['#3C93AF', '#F9AA41', '#4EBC95', '#325F74', '#0E272C', '#FFFFFF']

        labels = [item[0] for item in data]
        values = [item[1] for item in data]

        if chart_type == '1':  # Pie chart
            chart = go.Figure(
                data=[go.Pie(labels=labels, values=values,
                             marker=dict(colors=colors[:len(labels)]))],
                layout=go.Layout(title='Pie Chart: Selected Variables')
            )
        elif chart_type == '2':  # Bar chart
            chart = go.Figure(
                data=[go.Bar(x=labels, y=values,
                             marker=dict(color=colors[:len(labels)]))],
                layout=go.Layout(title='Bar Chart: Selected Variables',
                                 xaxis={'title': 'Categories'}, yaxis={'title': 'Count'})
            )
        else:
            chart = go.Figure()

        chart_html = chart.to_html(full_html=False)

        return render(request, 'customize.html', {
            'is_chart': 1,
            'chart': chart_html,
            'summary_data': data
        })

from analysis_module.adapters.dash_adapter import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from inventory_module.models import Product, Product_Inventory
from django.db.models import Sum  # Importar Sum de Django para agregaciones
from sales_module.models import Published_Product, Order

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Cambiar nombre a BarChart1
app = DjangoDash('BarChart2', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='bar-chart', animate=True, style={"backgroundColor": "#FFFFFF", 'color': '#FFFFFF'}),
    dcc.Slider(
        id='slider-bar',
        min=1,
        max=6,  # Hay 6 categorías de productos
        step=1,
        value=6,  # Valor inicial, muestra todas las categorías
        marks={i: str(i) for i in range(1, 7)},  # Marcas que van del 1 al 6
        updatemode='drag',
    ),
])

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('slider-bar', 'value')]
)
def update_bar_chart(value):
    # Obtener el total de productos en inventario agrupados por categoría
    categories = ['Fast Food', 'Healthy Options', 'Grilled & BBQ', 'Sides', 'Beverages', 'Desserts']
    
    # Obtener todas las órdenes
    
    orders_by_category = []
    counter = 0 
    for category in categories:
        for order in Order.objects.filter(customer_id = None):
            for product in order.products.all():
                if product.category == category:
                    counter = counter + product.quantity
        orders_by_category.append(counter)
        counter = 0

    # Limitar los datos según el valor del slider (muestra 'value' número de categorías)
    categories = categories[:value]
    orders_by_category = orders_by_category[:value]

    # Crear el gráfico de barras con los nuevos colores
    bar_chart = go.Bar(
        x=categories,
        y=orders_by_category,
        marker=dict(color=['#3C93AF', '#325F74', '#0E272C', '#4EBC95', '#F9AA41', '#FFFFFF']),  # Nuevos colores
    )

    layout = go.Layout(
        xaxis={'title': 'Product Categories'},
        yaxis={'title': 'Total Products sold in each category'},
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#F9F9F9',
        font=dict(color='black'),
    )

    return {'data': [bar_chart], 'layout': layout}

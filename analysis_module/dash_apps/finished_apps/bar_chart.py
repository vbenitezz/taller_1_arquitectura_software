from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from sales_module.models import Published_Product
from inventory_module.models import Product

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('BarChart', external_stylesheets=external_stylesheets)

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
    # Obtener los productos por categoría y contar
    fast_food = Product.objects.filter(category='Fast Food').count()
    healthy_options = Product.objects.filter(category='Healthy Options').count()
    grilled_bbq = Product.objects.filter(category='Grilled & BBQ').count()
    sides = Product.objects.filter(category='Sides').count()
    beverages = Product.objects.filter(category='Beverages').count()
    desserts = Product.objects.filter(category='Desserts').count()
    
    # Definir etiquetas y valores para el gráfico
    labels = ['Fast Food', 'Healthy Options', 'Grilled & BBQ', 'Sides', 'Beverages', 'Desserts']
    values = [fast_food, healthy_options, grilled_bbq, sides, beverages, desserts]

    # Limitar los datos según el valor del slider (muestra 'value' número de categorías)
    labels = labels[:value]
    values = values[:value]

    # Crear el gráfico de barras
    bar_chart = go.Bar(
        x=labels,
        y=values,
        marker=dict(color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']),  # Colores para cada barra
    )

    layout = go.Layout(
        title="Inventory by Category",
        xaxis={'title': 'Product Categories'},
        yaxis={'title': 'Product Count'},
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#F9F9F9',
        font=dict(color='black'),
    )

    return {'data': [bar_chart], 'layout': layout}


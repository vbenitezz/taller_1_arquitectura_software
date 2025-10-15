from analysis_module.adapters.dash_adapter import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from inventory_module.models import Published_Product

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimplePieChart', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='pie-chart', animate=True, style={"backgroundColor": "#FFFFFF", 'color': '#FFFFFF'}),
    dcc.Slider(
        id='slider-pie',
        min=1,  # Mostrar al menos una categoría
        max=2,  # Solo hay 2 categorías: 'Sale' y 'Donation'
        step=1,
        value=2,  # Valor inicial que muestra ambas categorías
        marks={1: '1', 2: '2'},  # Etiquetas del slider
        updatemode='drag',
    ),
])

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('slider-pie', 'value')]
)
def update_pie_chart(value):
    products_for_donation = sum([product.publish_quantity for product in Published_Product.objects.filter(publish_type='donation')])
    products_for_sale = sum([product.publish_quantity for product in Published_Product.objects.filter(publish_type='sale')])

    print('0'*100)
    print(products_for_donation)
    print(products_for_sale)
    labels = ['Sale', 'Donation']
    values = [products_for_sale, products_for_donation]

    # Limitar los datos según el valor del slider (muestra 'value' número de categorías)
    labels = labels[:value]
    values = values[:value]

    pie_chart = go.Pie(
        labels=labels,
        values=values,
        hole=0.1,  # Añadir un agujero para gráfico de dona
        marker=dict(colors=['#3C93AF', '#F9AA41']),  # Azul para venta y amarillo/naranja para donación
    )

    layout = go.Layout(
        paper_bgcolor='#FFFFFF',
        font=dict(color='black'),
    )

    return {'data': [pie_chart], 'layout': layout}

from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from sales_module.models import Published_Product
from sales_module.models import Order

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimplePieChart1', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='pie-chart', animate=True, style={"backgroundColor": "#FFFFFF", 'color': '#FFFFFF'}),
    dcc.Slider(
        id='slider-pie',
        min=1,  # El mínimo debe ser 1 para mostrar al menos un valor
        max=2,  # Ya que solo hay 2 categorías: "sold" y "donated"
        step=1,
        value=2,  # Valor inicial, muestra ambas categorías
        marks={1: '1', 2: '2'},  # Etiquetas del slider
        updatemode='drag',
    ),
])

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('slider-pie', 'value')]
)
def update_pie_chart(value):
    sold = 0
    donate = 0

    # Obtener todas las órdenes
    orders = Order.objects.all()
    for order in orders:
        for product in order.products.all():
            if order.customer_id is None:  # Ordenes sin cliente son donaciones
                donate += product.quantity
            else:  # Ordenes con cliente son ventas
                sold += product.quantity

    # Definir etiquetas y valores
    labels = ['Products sold', 'Products donated']
    values = [sold, donate]

    # Limitar los datos según el valor del slider (muestra 'value' número de categorías)
    labels = labels[:value]
    values = values[:value]

    # Crear el gráfico circular (pie chart)
    pie_chart = go.Pie(
        labels=labels,
        values=values,
        hole=0.1,  # Para agregar un pequeño agujero en el centro, como un gráfico de dona
        marker=dict(colors=['#3C93AF', '#F9AA41']),  # Colores del gráfico
    )

    layout = go.Layout(
        paper_bgcolor='#FFFFFF',
        font=dict(color='black'),
    )

    return {'data': [pie_chart], 'layout': layout}

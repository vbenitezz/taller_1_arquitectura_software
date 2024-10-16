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
        updatemode='drag',
    ),
])

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('slider-pie', 'value')]
)
def update_pie_chart(value):
    products_sold = Order.objects.filter(customer_id = None).count()
    products_donated = Order.objects.exclude(customer_id = None).count()

    labels = ['Products sold', 'Products donated']
    values = [products_sold, products_donated]

    # Limitar los datos según el valor del slider
    labels = labels[:value]
    values = values[:value]

    pie_chart = go.Pie(
        labels=labels,
        values=values,
        hole=0,  # Para agregar un pequeño agujero en el centro si quieres un gráfico de dona
    )

    layout = go.Layout(
        paper_bgcolor='#FFFFFF',
        font=dict(color='black'),
    )

    return {'data': [pie_chart], 'layout': layout}


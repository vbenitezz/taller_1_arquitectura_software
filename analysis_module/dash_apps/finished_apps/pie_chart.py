from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from sales_module.models import Published_Product

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimplePieChart', external_stylesheets=external_stylesheets)

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
    products_for_donation = Published_Product.objects.filter(publish_type='donation').count()
    products_for_sale = Published_Product.objects.filter(publish_type='sale').count()
    
    labels = ['Sale', 'Donation']
    values = [products_for_sale, products_for_donation]

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


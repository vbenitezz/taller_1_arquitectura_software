from django.urls import path
from .views import DisplayGraphicsView, CustomizeChartView
from analysis_module.dash_apps.finished_apps import pie_chart, pie_chart_1, bar_chart, bar_chart_1, bar_chart_2

app_name = 'analysis'

urlpatterns = [
    path('', DisplayGraphicsView.as_view(), name='display_graphics'),
    path('customize_chart/', CustomizeChartView.as_view(), name='customize_chart'),
]

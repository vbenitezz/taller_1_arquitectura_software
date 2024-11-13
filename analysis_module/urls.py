from django.urls import path
from . import views
from analysis_module.dash_apps.finished_apps import pie_chart, pie_chart_1, bar_chart, bar_chart_1, bar_chart_2

app_name = 'analysis' 
urlpatterns = [
    path('', views.display_graphics, name='display_graphics'),
    path('customize_chart/', views.customize_chart, name='customize_chart')
]
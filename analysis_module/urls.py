from django.urls import path
from . import views
from analysis_module.dash_apps.finished_apps import bar_chart, bar_chart_1

app_name = 'analysis' 
urlpatterns = [
    path('', views.home, name='analysis'),
]
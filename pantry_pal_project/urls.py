
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory_module.urls')),
    path('', include('sales_module.urls')),
    path('analysis/', include('analysis_module.urls')),
    path('access/', include('access_module.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

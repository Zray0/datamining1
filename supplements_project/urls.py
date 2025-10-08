from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls', namespace='inventory')),
    path('sales/', include('sales.urls')),
    path('analytics/', include('analytics.urls')),
]

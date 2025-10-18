from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    #path("", RedirectView.as_view(pattern_name="accounts:customer_login", permanent=False)),
    path("", RedirectView.as_view(pattern_name="accounts:login", permanent=False)),
    path('', include('inventory.urls', namespace='inventory')),
    path('', include('dashboards.urls')),
    path('sales/', include('sales.urls')),
    path('analytics/', include('analytics.urls')),
    path('dashboard/',include('dashboards.urls',namespace='dashboards')),
]

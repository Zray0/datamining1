# supplements_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect("admin:index")
    return redirect("dashboards:dashboard_home")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_redirect, name="home"),
    path("accounts/", include("accounts.urls")),
    path("analytics/", include("analytics.urls")),
    path("dashboards/", include("dashboards.urls")),
    path('sales/', include('sales.urls')),
    path('customer/', include('customer.urls')),
    path('cart/', include('cart.urls')),


]

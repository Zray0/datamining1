# dashboards/urls.py
from django.urls import path
from .views import dashboard_home
app_name = "dashboards"
urlpatterns = [path("", dashboard_home, name="dashboard_home")]

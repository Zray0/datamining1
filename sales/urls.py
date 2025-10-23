from django.urls import path
from . import views
from .views_dashboard import sales_dashboard

urlpatterns = [
      path("dashboard/", sales_dashboard, name="sales_dashboard"),
]

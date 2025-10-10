from django.urls import path
from . import views

app_name='dashboars'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('sales-chart/', views.dashboard_home, name='sales_chart'),  # or another view
    path('inventory-chart/', views.dashboard_home, name='inventory_chart'),
     
]

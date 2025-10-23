from django.urls import path
from .views import dashboard
from .views import dashboard, add_to_cart
urlpatterns = [
    path('dashboard/', dashboard, name='customer_dashboard'),
       path('add_to_cart/', add_to_cart, name='add_to_cart'),
]

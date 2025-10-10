from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from inventory.views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
app_name = 'inventory'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('',include(router.urls)),
]

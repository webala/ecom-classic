from django.urls import path
from .views import CategoryCreate, ProductCreate, dashboard

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('category/add', CategoryCreate.as_view(), name='category_create'),
    path('product/add', ProductCreate.as_view(), name='product_create')
]
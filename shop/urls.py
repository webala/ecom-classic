from django.urls import path
from .views import CategoryCreate, CategoryListView, ProductCreate, ProductDetail, ProductListView, dashboard, shop

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('category/add', CategoryCreate.as_view(), name='category_create'),
    path('product/add', ProductCreate.as_view(), name='product_create'),
    path('products', ProductListView.as_view(), name='products'),
    path('product/<pk>', ProductDetail.as_view(), name='product_detail'),
    path('', shop, name='shop'),
    path('category/<str:category_name>', CategoryListView.as_view(), name='product_per_category')
]
from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('category/add', CategoryCreate.as_view(), name='category_create'),
    path('product/add', ProductCreate.as_view(), name='product_create'),
    path('products', ProductListView.as_view(), name='products'),
    path('product/<pk>', ProductDetail.as_view(), name='product_detail'),
    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('order/process/<int:address_id>', process_order, name='process_order'),
    path('callback', mpesa_callback, name='mpesa_callback'),
    path('order/confirm/<request_id>', confirm_payment, name='confirm_payment'),
    path('transaction/<int:pk>', TransactionDetailView.as_view(), name='transaction'),
    path('', shop, name='shop'),
    path('category/<str:category_name>', CategoryListView.as_view(), name='product_per_category')
]
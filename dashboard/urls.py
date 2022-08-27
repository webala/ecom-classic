from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('products', dash_products, name='dash-products'),
    path('products/delete/<int:product_id>', delete_product, name='delete_product'),
    path('product/edit/<pk>', UpdateProduct.as_view(), name='update-product'),
    path('customers', CustomersView.as_view(), name='customers'),
    path('messages', MessagesView.as_view(), name='messages'),
    path('message/<pk>', MessageDetailView.as_view(), name='message'),
]
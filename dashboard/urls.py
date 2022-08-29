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
    path('reply', create_reply, name='create_reply'),
    path('mass_message', mass_message, name='mass_message'),
    path('transactions', TransactionsView.as_view(), name='transactions')
]
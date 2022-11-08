from django.urls import path
from .views import *

urlpatterns = [
    path('category/add', CategoryCreate.as_view(), name='category_create'),
    path('product/add', ProductCreate.as_view(), name='product_create'),
    path('products', ProductListView.as_view(), name='products'),
    path('about', about, name='about'),
    path('product/<pk>', ProductDetail.as_view(), name='product_detail'),
    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('order/process/<int:order_id>', process_order, name='process_order'),
    path('cart_items', cart_items, name='cart_items'),
    path('callback', mpesa_callback, name='mpesa_callback'),
    path('order/confirm/<request_id>', confirm_payment, name='confirm_payment'),
    path('transaction/<int:pk>', TransactionDetailView.as_view(), name='transaction'),
    path('contact', MessageCreate.as_view(), name='contact-us'),
    path('search', search_view, name='search'),
    path('', shop, name='shop'),
    path('category/<str:category_name>', CategoryListView.as_view(), name='product_per_category'),
    path('discount/create', DiscountCreateView.as_view(), name='discount-create'),
    path('book-success/<int:order_id>', book_success, name='book-success')

]
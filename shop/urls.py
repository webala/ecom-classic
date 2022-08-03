from django.urls import path
from .views import CategoryCreate, dashboard

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('category/add', CategoryCreate.as_view(), name='category_create')
]
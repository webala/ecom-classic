from django.shortcuts import render
# from django.urls import reverse
from django.views.generic.edit import CreateView

from shop.models import Category, Product

# Create your views here.


def dashboard(request):


    context = {}

    return render(request, 'dashboard.html', context)

class CategoryCreate(CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = '/shop/category/add'


class ProductCreate(CreateView):
    model = Product
    fields = ['category', 'name', 'price', 'inventory', 'image']
    template_name: str = 'product_form.html'
    success_url = '/shop/product/add'
    
from unicodedata import category
from django.shortcuts import render, get_object_or_404

# from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from shop.models import Category, Product

# Create your views here.


def dashboard(request):

    # get latest product entry in database
    latest_product = Product.objects.order_by("-id")[0]
    print("latest_product", latest_product)
    context = {"latest_product": latest_product}

    return render(request, "dashboard.html", context)


def shop(request):
    # get latest product entry in database
    latest_product = Product.objects.order_by("-id")[0]
    best_sellers = Product.objects.order_by("-id")[1:6]

    context = {"latest_product": latest_product, "best_sellers": best_sellers}

    return render(request, "shop.html", context)


class CategoryCreate(CreateView):
    model = Category
    fields = ["name"]
    template_name = "category_form.html"
    success_url = "/shop/category/add"


class ProductCreate(CreateView):
    model = Product
    fields = ["category", "name", "price", "inventory", "image"]
    template_name: str = "product_form.html"
    success_url = "/shop/product/add"


class ProductListView(ListView):
    model = Product
    template_name: str = "product_per_category.html"
    # context_object_name: str = 'products'


class CategoryListView(ListView):
    template_name: str = "product_per_category.html"

    def get_queryset(self):

        self.category = get_object_or_404(Category, name=self.kwargs["category_name"])
        return Product.objects.filter(category=self.category)

from django.shortcuts import render, get_object_or_404, redirect

# from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from .forms import ShippingAddressForm, CustomerForm
from shop.models import Category, Product
from shop.utils import get_cart_items

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


class ProductDetail(DetailView):
    model = Product
    template_name: str = 'product_detail.html'
    context_object_name: str = 'product'

def cart(request):
    data = get_cart_items(request)
    order = data['order']
    cart_items = data['cart_items']
    
    context = {
        'cart': order,
        'cart_items': cart_items
    }

    return render(request, 'cart.html', context)

def checkout(request):
    data = get_cart_items(request)
    order = data['order']
    cart_items = data['cart_items']
    
    customer_form = CustomerForm(request.POST or None)
    shipping_form = ShippingAddressForm(request.POST or None)

    #check if both forms are valid on post request
    if customer_form.is_valid() and shipping_form.is_valid():
        #save customer object
        customer = customer_form.save()
        #set customer object to customer field for shipping address object
        address = shipping_form.save(commit=False)
        address.customer = customer
        #save shipping address object
        address.save()
        #redirect to process order with the shipping address id
        return redirect('process_order', address_id=address.id)
        


    context = {
        'cart': order,
        'cart_items': cart_items
    }

    return render(request, )
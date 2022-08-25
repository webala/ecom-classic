from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from dashboard.utils import category_count, count_customers, count_messages, count_sales, get_products_worth, products_count
from shop.models import Category, Product
# Create your views here.


def dashboard(request):

    # get latest product entry in database
    products = products_count()
    categories = category_count()
    week_sales = count_sales(7)
    month_sales = count_sales(30)
    messages = count_messages()
    customers = count_customers()
    products_worth = get_products_worth()

    context = {
        'products': products,
        'categories': categories,
        'week_sales': week_sales,
        'month_sales': month_sales,
        'customer_messages': messages,
        'customers': customers,
        'products_worth': products_worth
    }

    return render(request, "dashboard.html", context)

def dash_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'total_products': products_count(),
        'total_categories': category_count()
    }

    return render(request, 'dash/products.html', context)

def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if product:
        product.delete()
    
    return redirect('dash-products')

class UpdateProduct(UpdateView):
    model = Product
    fields = ['name', 'price', 'category', 'inventory', 'image']
    template_name: str = 'dash/product_update.html'
    success_url: str = '/dashboard/products'
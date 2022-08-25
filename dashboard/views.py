from django.shortcuts import render
from dashboard.utils import category_count, count_customers, count_messages, count_sales, get_products_worth, products_count
from shop.models import Product
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
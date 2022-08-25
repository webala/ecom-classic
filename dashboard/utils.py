from shop.models import Customer, Message, Product, Category, Order
from datetime import datetime, timedelta


def products_count():
    return len(list(Product.objects.all()))

def category_count():
    return len(list(Category.objects.all()))

def count_sales(days):
    start_date = datetime.now()
    end_date = start_date - timedelta(days=days)
    
    orders = Order.objects.filter(
        date_created__range=[start_date, end_date],
        processed=True
    )

    number_of_sales = len(orders)
    sales_amount = sum([order.cart_total for order in orders])
    return {'number_of_sales': number_of_sales, 'sales_amount': sales_amount}

def count_messages():
    return len(list(Message.objects.filter(read=False)))

def count_customers():
    return len(list(Customer.objects.all()))

def get_products_worth():
    return sum([product.price for product in Product.objects.all()])
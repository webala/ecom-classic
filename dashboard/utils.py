import os
from shop.models import Customer, Message, Product, Category, Order, TransactionDetails
from datetime import datetime, timedelta
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

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

def get_graph_data():
    transactions = TransactionDetails.objects.all()


def send_email(subject, body, receiver):
    email_sender = 'webdspam@gmail.com'
    email_password = os.getenv('GMAIL_L0GIN')
    email_receiver = receiver

    #Instantiate EmailMessage class
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    #Use SSL to add a layer of security
    context = ssl.create_default_context()

    #Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    
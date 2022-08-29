from dataclasses import field
from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from django.views.generic.edit import UpdateView
from django.views.generic import ListView, DetailView
from dashboard.utils import category_count, count_customers, count_messages, count_sales, get_products_worth, products_count, send_email
from shop.models import Category, Customer, Message, Product, Reply, TransactionDetails
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

class CustomersView(ListView):
    model = Customer
    template_name = 'dash/customers.html'
    fields = ['first_name', 'last_name', 'phone', 'email']
    context_object_name: str = 'customers'

class MessagesView(ListView):
    model = Message
    template_name: str = 'dash/messages.html'
    fields = ['name', 'email', 'message', 'date', 'read']
    context_object_name: str = 'customer_messages'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'dash/message_detail.html'
    context_object_name: str = 'customer_message'

    def get_object(self):

        #Mark message as read
        obj = super().get_object()
        obj.read = True
        obj.save()
        return obj

    def get_context_data(self, **kwargs):

        #get message replies if any
        context = super().get_context_data(**kwargs)
        message = context['customer_message']
        replies = Reply.objects.filter(message=message)
        context['replies'] = replies 
        return context

class TransactionsView(ListView):
    model = TransactionDetails
    template_name: str = 'dash/transactions.html'
    context_object_name = 'transactions'
    fields = ['order', 'receipt_number', 'amount', 'phone_number', 'date', 'is_successful']


def create_reply(request):
    if request.method == 'POST':
        print('post request received')
        data = request.POST
        subject = data.get('subject')
        body = data.get('body')
        message_id = data.get('customer_message_id')
        message = Message.objects.get(id=message_id)
        receiver = message.email

        send_email(subject, body, receiver)

        Reply.objects.create(
            subject=subject,
            message=message,
            body=body
        )
        return redirect('/dashboard/message/{}'.format(message_id))
    else:
        print('method not allowed')
        return HttpResponseNotAllowed('Method not allowed')


def mass_message(request):
    customers = Customer.objects.all()
    data = request.POST
    subject = data.get('subject')
    body = data.get('body')

    for customer in customers:
        customer_mail = customer.email
        send_email(subject, body, customer_mail)
    
    return redirect('/dashboard/messages')

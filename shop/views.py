from itertools import product
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from .forms import ShippingAddressForm, CustomerForm
from shop.models import (
    CartItem,
    Category,
    Order,
    Product,
    ShippingAddress,
    TransactionDetails,
)
from shop.utils import get_cart_items, initiate_stk_push

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
    template_name: str = "product_detail.html"
    context_object_name: str = "product"


def cart(request):
    data = get_cart_items(request)
    order = data["order"]
    cart_items = data["cart_items"]

    context = {"cart": order, "cart_items": cart_items}

    return render(request, "cart.html", context)


def checkout(request):
    data = get_cart_items(request)
    order = data["order"]
    cart_items = data["cart_items"]

    customer_form = CustomerForm(request.POST or None)
    shipping_form = ShippingAddressForm(request.POST or None)

    # check if both forms are valid on post request
    if customer_form.is_valid() and shipping_form.is_valid():
        # save customer object
        customer = customer_form.save()
        # set customer object to customer field for shipping address object
        address = shipping_form.save(commit=False)
        address.customer = customer
        # save shipping address object
        address.save()
        # redirect to process order with the shipping address id
        return redirect("process_order", address_id=address.id)

    context = {
        "cart": order,
        "cart_items": cart_items,
        "customer_form": customer_form,
        "shipping_form": shipping_form,
    }

    return render(request, "checkout.html", context)


def process_order(request, address_id):
    shipping_address = ShippingAddress.objects.get(id=address_id)
    customer_phone = shipping_address.customer.phone
    data = get_cart_items(request)
    cookie_cart_items = data["cart_items"]

    # populate database with order and cart items from the cookies
    order = Order.objects.create(shipping_address=shipping_address)
    for item in cookie_cart_items:
        product_id = item["product"]["id"]
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.create(product=product, quantity=item["quantity"])
        cart_item.cart = order
        cart_item.save()

    if request.method == "POST":
        amount = order.cart_total
        phone = request.POST["phone"]
        if phone == customer_phone:
            response_data = initiate_stk_push(customer_phone, amount)
            print(response_data)
            request_id = response_data["chechout_request_id"]
            TransactionDetails.objects.create(request_id=request_id, order=order)
            return redirect("confirm_payment", request_id=request_id)
        else:
            customer = shipping_address.customer
            customer.phone = phone
            customer.save()
            response_data = initiate_stk_push(phone, amount)
            print(response_data)
            request_id = response_data["chechout_request_id"]
            TransactionDetails.objects.create(request_id=request_id, order=order)
            return redirect("confirm_payment", request_id=request_id)
    context = {"phone": customer_phone}

    return render(request, "process_order.html", context)


@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        body = request_data.get("Body")
        result_code = body.get("stkCallback").get("ResultCode")

        if result_code == 0:
            print("Payment successful")
            request_id = body.get("stkCallback").get("CheckoutRequestID")
            metadata = body.get("stkCallback").get("CallbackMetadata").get("Item")

            for data in metadata:
                if data.get("Name") == "MpesaReceiptNumber":
                    receipt_number = data.get("Value")
                elif data.get("Name") == "Amount":
                    amount = data.get("Value")
                elif data.get("Name") == "PhoneNumber":
                    phone_number = data.get("Value")
            print("receipt:", receipt_number)
            print("amouont: ", amount)
            print("request_id: ", request_id)
            transaction = TransactionDetails.objects.get(request_id=request_id)
            transaction.receipt_number = receipt_number
            transaction.amount = amount
            transaction.phone_number = str(phone_number)
            transaction.is_finished = True
            transaction.is_succesful = True
            transaction.save()

            # context = {
            #     'transaction': transaction
            # }
            return HttpResponse('Ok')

def confirm_payment(request, request_id):
    transaction = TransactionDetails.objects.get(request_id = request_id)

    context = {
        'transaction': transaction
    }
    return render(request, 'confirm_payment.html', context)

class TransactionDetailView(DetailView):
    model = TransactionDetails
    template_name: str = "transaction.html"
    context_object_name: str = "transaction"

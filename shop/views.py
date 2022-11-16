from multiprocessing import context
from django.contrib.messages.views import SuccessMessageMixin
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from .forms import MessageForm, ShippingAddressForm, CustomerForm, ProductCreateForm
from shop.models import (
    CartItem,
    Category,
    Discount,
    Message,
    Order,
    Product,
    ShippingAddress,
    TransactionDetails,
    Discount
)
from shop.utils import get_cart_items, initiate_stk_push, auth, email, password, get_image_url, upload_product_image
from django.core.paginator import Paginator

# Create your views here.


def home(reqeust):
    discounts = Discount.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()
    p = Paginator(products, 15)
    page = reqeust.GET.get('page')
    page_obj = p.get_page(page)

    context = {
        'discounts': discounts,
        'page_obj': page_obj,
        'categories': categories
    }
    
    return render(reqeust, 'home.html', context)


def shop(request):
    # get latest product entry in database
    latest_product = Product.objects.order_by("-id")[1:6]
    categories = Category.objects.all()
    discounts = Discount.objects.all()
    context = {
        "latest_product": latest_product,
        "categories": categories,
        "discounts": discounts,
    }

    return render(request, "shop.html", context)


class CategoryCreate(CreateView):
    model = Category
    fields = ["name"]
    template_name = "category_form.html"
    success_url = "/shop/category/add"


class ProductCreate(CreateView):
    model = Product
    # fields = ["category", "name", "price", "inventory"]
    template_name: str = "product_form.html"
    # success_url = "/shop/product/add"
    form_class = ProductCreateForm

    def post(self, request, *args: str, **kwargs):
        product_create_form = ProductCreateForm(request.POST, request.FILES)
        if product_create_form.is_valid():
            image = request.FILES.get('image')
            product = product_create_form.save(commit=False)
            
            
            image_data = upload_product_image(image)
            filaname = image_data['filename']
            image_url = image_data['image_url']

            product.image_filename = filaname
            product.image_url = image_url
            product.save()
            return redirect('product_create')
        


class ProductListView(ListView):
    model = Product
    template_name: str = "product_per_category.html"
    # context_object_name: str = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context["categories"] = categories
        return context


class CategoryListView(ListView):
    template_name: str = "product_per_category.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs["category_name"])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context["categories"] = categories
        return context


class ProductDetail(DetailView):
    model = Product
    template_name: str = "product_detail.html"
    context_object_name: str = "product"


class DiscountCreateView(CreateView):
    model = Discount
    template_name: str = "discount_create.html"
    fields = ["product", "percentage"]
    success_url: str = "/shop/discount/create"


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
        payment = request.POST.get("payment")
        # save customer object
        customer = customer_form.save()
        # set customer object to customer field for shipping address object
        address = shipping_form.save(commit=False)
        address.customer = customer
        # save shipping address object
        address.save()

        # populate database with order and cart items from the cookies
        order = Order.objects.create(shipping_address=address)
        for item in cart_items:
            product_id = item["product"]["id"]
            product = Product.objects.get(id=product_id)
            cart_item = CartItem.objects.create(product=product, quantity=item["quantity"])
            cart_item.cart = order
            cart_item.save()

        if payment == 'now':
            # redirect to process order with the shipping address id
            return redirect("process_order", order_id=order.id)
        else:
            return redirect('book-success', order_id=order.id)

    context = {
        "cart": order,
        "cart_items": cart_items,
        "customer_form": customer_form,
        "shipping_form": shipping_form,
    }

    return render(request, "checkout.html", context)

def book_success(request, order_id):
    order = Order.objects.get(id=order_id)
    cart_items = order.cartitem_set.all()

    context = {
      'order': order,
      'cart_items': cart_items  
    }
    
    return render(request, 'book_success.html', context)


def process_order(request, order_id):
    order = Order.objects.get(id=order_id)
    customer_phone = order.shipping_address.customer.phone

    if request.method == "POST":
        print("post req ...")
        amount = order.cart_total
        phone = request.POST.get("phone")
        if phone == customer_phone:
            response_data = initiate_stk_push(customer_phone, amount)
            print("response", response_data)
            print(response_data)
            request_id = response_data["chechout_request_id"]
            TransactionDetails.objects.create(request_id=request_id, order=order)
            return redirect("confirm_payment", request_id=request_id)
        else:
            customer = order.shipping_address.customer
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

            order = transaction.order
            order.processed = True
            order.save()

            # context = {
            #     'transaction': transaction
            # }
            return HttpResponse("Ok")


def confirm_payment(request, request_id):
    transaction = TransactionDetails.objects.get(request_id=request_id)
    order = transaction.order
    order_items = order.cartitem_set.all()
    context = {"transaction": transaction, 'order_items': order_items}
    return render(request, "confirm_payment.html", context)


def cart_items(request):
    cart_data = get_cart_items(request)
    cart_items = cart_data["order"]["cart_items"]
    cart_total = cart_data["order"]["cart_total"]

    return JsonResponse({"cart_items": cart_items, "cart_total": cart_total})


def about(request):
    return render(request, "about.html")


class TransactionDetailView(DetailView):
    model = TransactionDetails
    template_name: str = "transaction.html"
    context_object_name: str = "transaction"


class MessageCreate(SuccessMessageMixin, CreateView):
    # model = Message
    template_name: str = "message_form.html"
    # fields = ['name', 'email', 'message']
    form_class = MessageForm
    success_message: str = "Message sent. We will use your email to get back to you."
    success_url: str = "/shop"


def search_view(request):
    if request.method == "POST":
        query = request.POST["search_query"]
        products = Product.objects.filter(name__contains=query)
        category = Category.objects.filter(name__contains=query).first()
        print(category)
        category_products = Product.objects.filter(category=category)
        
        context = {
            "products": products,
            "search_value": query,
            "category_products": category_products
        }
        return render(request, "search.html", context)
    return render(request, "search.html")

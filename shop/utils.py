import json
import os
from .models import Product
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()


#Get cart cookie and return order and order items object
def get_cart_items(request):
    try:
        cart_cookie_data = json.loads(request.COOKIES['cart'])
    except:
        cart_cookie_data = {}

    order = {'cart_items': 0, 'cart_total': 0}
    order_items = []

    for item in cart_cookie_data:
        product = Product.objects.get(id=item)
        total = product.price * cart_cookie_data[item]['quantity']

        order['cart_items'] += cart_cookie_data[item]['quantity']
        order['cart_total'] += total
        
        cart_item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'category': product.category.name,
                'image_url': product.image_url
            },
            'quantity': cart_cookie_data[item]['quantity'],
            'item_total': total
        }

        order_items.append(cart_item)
    
    return {'order': order, 'cart_items': order_items}

#Function to generate daraja access token
def get_access_token():
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    response = requests.get(settings.DARAJA_AUTH_URL, auth = HTTPBasicAuth(consumer_key, consumer_secret))

    json_res = response.json()
    access_token = json_res['access_token']
    return access_token


def initiate_stk_push(phone, amount):
    pass
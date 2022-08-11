import json
import os
from urllib import response
from .models import Product
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from datetime import datetime
import base64
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

#function to format date time
def format_date_time():
    current_time = datetime.now()
    formated_time = current_time.strftime('%Y%m%d%H%M%S')
    return formated_time


#function to generate password string
def generate_password(dates):
    data_to_encode = str(settings.BUSINESS_SHORT_CODE) + settings.LIPANAMPESA_PASSKEY + dates
    encoded_string = base64.b64encode(data_to_encode.encode())
    decoded_passkey = encoded_string.decode('utf-8')

    return decoded_passkey

#function to initiate stk push for mpesa payment
def initiate_stk_push(phone, amount):
    access_token = get_access_token()
    formated_time = format_date_time()
    password = generate_password(formated_time)

    headers = {
        'Authorization': 'Bearer %s' % access_token
    }

    payload = {    
            "BusinessShortCode": settings.BUSINESS_SHORT_CODE,    
            "Password": password,    
            "Timestamp": formated_time,    
            "TransactionType": "CustomerPayBillOnline",    
            "Amount": 1,    
            "PartyA":phone,    
            "PartyB":"174379",    
            "PhoneNumber":phone,    
            "CallBackURL":"https://c87c-105-163-1-221.eu.ngrok.io/shop/order/confirm",    
            "AccountReference":"ECOM CLASSIC",    
            "TransactionDesc":"Make Payment"
        }

    response = requests.post(
        settings.API_RESOURCE_URL, headers=headers, json=payload
    )

    string_response = response.text
    string_object = json.loads(string_response)

    if 'errorCode' in string_object:
        print('Error: ', string_object)
        return string_object
    else:
        data = {
                'merchant_request_id' :string_object['MerchantRequestID'],
                'chechout_request_id' :string_object['CheckoutRequestID'],
                'response_code' :string_object['ResponseCode'],
                'response_description' :string_object['ResponseDescription'],
                'customer_meaasge' :string_object['CustomerMessage'],
            }
    return data
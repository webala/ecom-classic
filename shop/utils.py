import json
import os
import pyrebase
import secrets
from PIL import Image
from io import BytesIO
from urllib import response
from .models import Product
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.core.files import File
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
        if product.has_discount:
            product_price = product.discount.new_price
        else:
            product_price = product.price
            
        total = product_price * cart_cookie_data[item]['quantity']

        order['cart_items'] += cart_cookie_data[item]['quantity']
        order['cart_total'] += total
        
        cart_item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product_price,
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
    print('get token called')
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    print('consumer_key', consumer_key, 'consumer_secret', consumer_secret)
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
    print('stk push called')
    
    access_token = get_access_token()
    print('access token', access_token)
    formated_time = format_date_time()
    print(' formated_time', formated_time)
    password = generate_password(formated_time)
    print(' password', password)
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
            "CallBackURL":"https://abac-41-80-96-106.eu.ngrok.io/shop/callback",    
            "AccountReference":"ECOM CLASSIC",    
            "TransactionDesc":"Make Payment"
        }

    response = requests.post(
        settings.API_RESOURCE_URL, headers=headers, json=payload
    )
    print('response: ', response)
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

#firebase configuration
firebase_config = {
  'apiKey': "AIzaSyBlUL0zRZOWZ3bT-5N2QPUjm5sG08luiZw",
  'authDomain': "ecom-classic.firebaseapp.com",
  'projectId': "ecom-classic",
  'storageBucket': "ecom-classic.appspot.com",
  'messagingSenderId': "690560719255",
  'appId': "1:690560719255:web:d1e5f7b1dce3eb22c24cd2",
  'measurementId': "G-H6MJJKY3YE",
   "databaseURL": "",
}

firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()

auth = firebase.auth()
email = os.getenv('FIREBASE_EMAIL')
password = os.getenv("FIREBASE_PASSWORD")


#Compress the image file
def compress_image(image, ):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, "JPEG", quality=60)
    new_image = File(im_io, name=image.name)
    return new_image

def upload_product_image(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.name)
    filename = random_hex + f_ext
    file.name = filename
    image = compress_image(file)
    directory = f'products/{filename}'
    user = auth.sign_in_with_email_and_password(email, password)
    print('user: ', user)
    storage.child(directory).put(image, user['idToken'])
    image_url = get_image_url(filename, user)
    return {'filename':filename, 'image_url': image_url}

def get_image_url(filename, user):
    path = f'products/{filename}'
    url = storage.child(path).get_url(user["idToken"])
    return url
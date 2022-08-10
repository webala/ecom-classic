import json
from .models import Product


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


def initiate_stk_push(phone, amount):
    pass
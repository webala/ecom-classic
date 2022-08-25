
from django.db import models

# Create your models here.


#Products will be grouped into different categories.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    inventory = models.IntegerField()
    image = models.ImageField()
    # is_limited = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    @property
    def image_url(self):
        return self.image.url

# class Rating(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     rating = models.IntegerChoices()


#customer Details
class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=12)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


#Delivery Address for products
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.CharField(max_length=20)
    estate = models.CharField(max_length=20)
    house_no = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.location + ' ' + self.estate

#This model will translate to cart in the client side
class Order(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)

    #this function returns the number of items in an order(cart)
    @property
    def cart_items(self):
        cart_items = self.cartitem_set.all()
        return sum([item.quantity for item in cart_items])
    
    #This function return the total price of the order
    @property
    def cart_total(self):
        cart_items = self.cartitem_set.all()
        return sum([item.item_total for item in cart_items])


#individual items in an order(cart)
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()


    @property
    def item_total(self):
        return self.quantity * self.product.price

#Transaction details for paymetents made
class TransactionDetails(models.Model):
    request_id = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    receipt_number = models.CharField(max_length=20, null=True, blank=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
    is_succesful = models.BooleanField(default=False)

class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    



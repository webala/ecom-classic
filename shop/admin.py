from django.contrib import admin

from shop.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ShippingAddress)
admin.site.register(Customer)
admin.site.register(TransactionDetails)
admin.site.register(Message)
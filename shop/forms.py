
from django import forms
from .models import Customer, Discount, Message, ShippingAddress, Product

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone']


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['location', 'estate', 'house_no']

class MessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Message
        fields = ['name', 'email', 'message']


class DiscountCreateForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['product', 'percentage']
    
class ProductCreateForm(forms.ModelForm):
    image = forms.FileField()
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'inventory', 'image']
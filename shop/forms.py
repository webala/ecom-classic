from django import forms

class ProductForm (forms.ModelForm):
    class Meta:
        model = Product
        
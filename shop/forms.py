from dataclasses import field
from django import forms
from .models import Category, Product

class ProductForm (forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'inventory', 'image']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        field = ['name']
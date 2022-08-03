from django.shortcuts import render
from django.views.generic.edit import CreateView

from shop.models import Category

# Create your views here.


def dashboard(request):


    context = {}

    return render(request, 'dashboard.html', context)

class CategoryCreate(CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'

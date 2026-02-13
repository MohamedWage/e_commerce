from django.shortcuts import render
from django.views.generic import ListView
from account.models import *
# Create your views here.


class ProductView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

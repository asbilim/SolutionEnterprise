from django.shortcuts import render
from .models import Product


def index(request):
    
    all_products = Product.objects.all()
    
    return render(request,'shop/index.html',{'products':all_products})


def shop(request):
    
    
    all_products = Product.objects.all()
    
    return render(request,'shop/shop.html',{'products':all_products})
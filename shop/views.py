from django.shortcuts import render
from .models import Product,Contact,Request


def index(request):
    
    all_products = Product.objects.all()
    
    return render(request,'shop/index.html',{'products':all_products})


def shop(request):
    
    
    all_products = Product.objects.all()
    
    return render(request,'shop/shop.html',{'products':all_products})


def about(request):
    
    
    all_products = Product.objects.all()
    
    return render(request,'shop/about.html',{'products':all_products})


def contact(request):
    
    
    all_products = Product.objects.all()

    if request.method == 'POST':

        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            contact = Contact(email=email,subject=subject,message=message)
            contact.notify()
            contact.save()
        except Exception as e:
            print(e)
    
    return render(request,'shop/contact.html',{'products':all_products})


def product_detail(request,slug):

    product = Product.objects.get(slug=slug)

    if request.method == 'POST':

        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        try:
            request = Request(email=email,phone_number=phone_number,product=product)
            request.notify()
            request.save()
        except Exception as e:
            print(e)
    
    return render(request,'shop/product-detail.html',{'product':product})
from django.urls import path,include
from .views import index,shop,product_detail

urlpatterns = [
    path('',index,name="home-index-page"),
    path('home',shop,name="home-shop-page"),
    path('products/<str:slug>',product_detail,name="shop-details"),
    
]

from django.urls import path,include
from .views import index,shop,about

urlpatterns = [
    path('',index,name="home-index-page"),
    path('home',shop,name="home-shop-page"),
    path("__reload__/", include("django_browser_reload.urls")),
]

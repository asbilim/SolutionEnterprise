from django.urls import path
from .views import home,details

urlpatterns = [
    path('home',home,name="home"),
    path('details/<str:slug>/',details,name="blog-details")
]

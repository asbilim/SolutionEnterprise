from django.contrib import admin
from .models import Product,Testimonial,ImageGallery

models = [Product,Testimonial,ImageGallery]

for model in models:
    admin.site.register(model)
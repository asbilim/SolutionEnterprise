from django.contrib import admin
from .models import Product,Testimonial

models = [Product,Testimonial]

for model in models:
    admin.site.register(model)
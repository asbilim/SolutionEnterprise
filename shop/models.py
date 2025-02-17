from django.db import models
from django.utils.text import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from meta.models import ModelMeta
import os
from django.utils import timezone
from solution.storage_backends import MediaStorage

def send_html_email(subject, template_location, datas):
    html_message = render_to_string(template_location, datas)
    plain_message = strip_tags(html_message)
    from_email = os.getenv('EMAIL_HOST_USER')
    to = "contact@solutionepi.com"  # Consider moving this to settings or env

    send_mail(
        subject,
        plain_message,
        from_email,
        [to],
        html_message=html_message,
    )
    

class ImageGallery(models.Model):

    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="gallery/",
        storage=MediaStorage()
    )

    def __str__(self):
        return self.name
    
class Product(models.Model,ModelMeta):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to="products/",
        storage=MediaStorage()
    )
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    sizable = models.BooleanField(default=False)
    downloadable = models.BooleanField(default=False)
    gallery = models.ManyToManyField(ImageGallery)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    _metadata = {
        'title': 'name',
        'description': 'description',
        'image': 'get_absolute_image_url',
        'og_type': 'article',  # OpenGraph type
        'og_description': 'description',
        'og_image': 'get_absolute_image_url',
        'twitter_card': 'summary_large_image',  # Twitter card type
        'twitter_site': '@solutionepi',  # Site's Twitter handle
        'twitter_creator': '@solutionepi',  # Author's Twitter handle
        'twitter_title': 'name',
        'twitter_description': 'description',
        'twitter_image': 'get_absolute_image_url',
    }

    def get_absolute_image_url(self):
        if self.image:
            return self.image.url  # Adjust accordingly if you're using a full UR
    
    def __str__(self):
        
        return self.name
    
class Testimonial(models.Model):
    
    message = models.TextField()
    author = models.CharField(max_length=255)
    image = models.ImageField(upload_to="testimonials/")
    position = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.author} from {self.position}"
    

class Contact(models.Model):

    subject = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.message
    
    def notify(self):

        send_html_email(
            self.subject,
            "shop/emails/contact.html",
            {
                "email": self.email,
                "message": self.message,
            },
        )

    
    
class Request(models.Model):

    phone_number = models.CharField(max_length=255)
    email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.email
    
    def notify(self):

        send_html_email(
            "New request for a product",
            "shop/emails/request.html",
            {
                "email": self.email,
                "phone_number": self.phone_number,
                "product":self.product
            },
        )

    
 
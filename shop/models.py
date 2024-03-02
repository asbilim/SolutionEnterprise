from django.db import models
from django.utils.text import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_html_email(subject,template_location, datas):

    html_message = render_to_string(template_location, datas)
    plain_message = strip_tags(html_message)
    from_email = "noreply@solutionepi.com"
    to = "info@solutionepi.com"

    send_mail(
        subject,
        plain_message,
        from_email,
        [to],
        html_message=html_message,
        auth_user="noreply@solutionepi.com",
        auth_password="wgjM0AkK?lacho",
        connection=None,
    )
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="lachoshop/images/products/")
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    sizable = models.BooleanField(default=False)
    downloadable = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        
        return self.name
    
class Testimonial(models.Model):
    
    message = models.TextField()
    author = models.CharField(max_length=255)
    image = models.ImageField(upload_to="testimonials/")
    position = models.CharField(max_length=255)
    
    def __str__(self):
        
        return f"{self.name} from {self.position}"
    
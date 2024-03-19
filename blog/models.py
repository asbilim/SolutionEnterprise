from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

class Category(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True,upload_to="category/")
    def __str__(self) :
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Article(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    image = models.ImageField(upload_to="blog-images/")
    title=models.CharField(max_length=200)
    content=CKEditor5Field('Text', config_name='extends')
    description = models.TextField(blank=True,null=True)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):

        return self.title
    
    
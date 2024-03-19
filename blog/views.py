from django.shortcuts import render
from .models import Article,Category
def home(request):

    blogs = Article.objects.all()
    categories = Category.objects.all()

    return render(request, 'blog/home.html', {'blogs':blogs,'categories':categories[:3],'reverse':blogs.reverse(),'recent':blogs[:3]})


def details(request,slug):

    try:
        blog = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        return 

    return render(request, 'blog/details.html',{'blog':blog})
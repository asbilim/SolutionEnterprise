from django.shortcuts import render

def handler500(request):
    return render(request, '500.html', status=500)

def handler404(request, exception):
    return render(request, '404.html', status=404) 
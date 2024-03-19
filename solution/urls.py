from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from shop.views import about,contact,blog
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("shop.urls")),
    path('about/',about),
    path('contact/',contact),
    path('blog/',include("blog.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    # path("__reload__/", include("django_browser_reload.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
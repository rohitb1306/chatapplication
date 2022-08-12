from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/',include('chat.urls')),
    path('',include('home.urls')),
    path("accounts/",include('django.contrib.auth.urls')),
    path("accounts/",include('account.urls')),
    path('ckeditor',include('ckeditor_uploader.urls'),)
    

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

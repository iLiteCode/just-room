"""
hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information, please see:
https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import krishna.views as views
from django.urls import include, path

urlpatterns = [
    
    # Admin
    path('admin/', admin.site.urls),

    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('krishna.urls')),
    path('user/', include('user.urls', namespace='user')),
    
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

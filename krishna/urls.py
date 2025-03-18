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
    # Public Pages
    path('', views.homepage, name="homepage"),
    path('home', views.homepage, name="homepage"),
    path('about', views.aboutpage, name="aboutpage"),
    path('contact', views.contactpage, name="contactpage"),

    # User Pages
    path('user/bookings', views.user_bookings, name="dashboard"),
    path('user/book-room', views.book_room_page, name="bookroompage"),
    path('user/book-room/book', views.book_room, name="bookroom"),

    # Staff Pages
    
    
    path('staff/panel', views.panel, name="staffpanel"),
    path('staff/allbookings', views.all_bookings, name="allbookings"),
    path('staff/panel/add-new-location', views.add_new_location, name="addnewlocation"),
    path('staff/panel/edit-room', views.edit_room, name="editroom"),
    path('staff/panel/add-new-room', views.add_new_room, name="addroom"),
    path('staff/panel/edit-room/edit', views.edit_room, name="editroomaction"),
    path('staff/panel/view-room', views.view_room, name="viewroom"),

   

    # Admin

    path('i18n/', include('django.conf.urls.i18n')),

    path('', views.Check_list, name='check_list'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('username', 'password', 'paid_member','name','phone')})
UserAdmin.fieldsets = tuple(fields)
admin.site.register(User, UserAdmin)
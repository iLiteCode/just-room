from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Define the fields to display in the admin list view
    list_display = ('username', 'name', 'phone', 'email', 'is_staff', 'is_active', 'paid_member')
    
    # Add filters to easily sort verified vs unverified users
    list_filter = ('is_active', 'is_staff', 'paid_member')
    
    # Enable search by username, email, name, and phone
    search_fields = ('username', 'email', 'name', 'phone')
    
    # Customize the fieldsets for the add/edit form
    fieldsets = (
        (None, {'fields': ('username', 'password', 'name', 'phone', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Membership', {'fields': ('paid_member',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'phone', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'paid_member'),
        }),
    )
    
    # Optional: Prevent editing of unverified users (uncomment to enable)
    # def has_change_permission(self, request, obj=None):
    #     if obj is not None and not obj.is_active:
    #         return False  # Deny editing for unverified users
    #     return super().has_change_permission(request, obj)

    # Optional: Customize the queryset to highlight unverified users
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs  # You could filter here, e.g., qs.filter(is_active=True) to show only verified users

# Register the custom UserAdmin
admin.site.register(User, UserAdmin)
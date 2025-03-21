from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import redirect
from django.utils.html import format_html
from .models import User, HotelStaff, Maintainer

class UserAdmin(BaseUserAdmin):
    list_display = (
        'username', 'name', 'phone', 'email', 'is_staff', 'is_verified_link', 'paid_member',
        'profile_image_preview', 'aadhar_image_preview', 'pancard_image_preview'
    )
    list_editable = ('name', 'phone', 'email', 'paid_member')
    list_filter = ('is_verified', 'is_staff', 'paid_member')
    search_fields = ('username', 'email', 'name', 'phone')
    
    fieldsets = (
        (None, {'fields': ('username', 'password', 'name', 'phone', 'email')}),
        ('Personal Documents', {'fields': ('profile_image', 'aadhar_image', 'pancard_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Membership', {'fields': ('paid_member',)}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'phone', 'email', 'password1', 'password2', 'is_staff', 'is_verified', 
                       'paid_member', 'profile_image', 'aadhar_image', 'pancard_image'),
        }),
    )
    
    def is_verified_link(self, obj):
        status = "Verified" if obj.is_verified else "Not Verified"
        action = "Unverify" if obj.is_verified else "Verify"
        return format_html('<a href="{}">{}</a> ({})', f'/admin/user/user/{obj.pk}/toggle_verified/', action, status)
    is_verified_link.short_description = 'Verification'

    def profile_image_preview(self, obj):
        return format_html('<img src="{}" width="50" />', obj.profile_image.url) if obj.profile_image else "No Image"
    profile_image_preview.short_description = 'Profile Img'

    def aadhar_image_preview(self, obj):
        return format_html('<img src="{}" width="50" />', obj.aadhar_image.url) if obj.aadhar_image else "No Image"
    aadhar_image_preview.short_description = 'Aadhar Img'

    def pancard_image_preview(self, obj):
        return format_html('<img src="{}" width="50" />', obj.pancard_image.url) if obj.pancard_image else "No Image"
    pancard_image_preview.short_description = 'Pancard Img'

    actions = ['verify_users', 'unverify_users']

    def verify_users(self, request, queryset):
        updated = queryset.filter(is_verified=False).update(is_verified=True)
        self.message_user(request, f"{updated} users have been verified.")
    verify_users.short_description = "Verify selected users"

    def unverify_users(self, request, queryset):
        updated = queryset.filter(is_verified=True).update(is_verified=False)
        self.message_user(request, f"{updated} users have been unverified.")
    unverify_users.short_description = "Unverify selected users"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/toggle_verified/', self.admin_site.admin_view(self.toggle_verified), name='toggle_verified'),
        ]
        return custom_urls + urls

    def toggle_verified(self, request, user_id):
        user = self.get_object(request, user_id)
        if user:
            user.is_verified = not user.is_verified
            user.save()
            self.message_user(request, f"User {user.username} verification status updated to {user.is_verified}.")
        return redirect('admin:user_user_changelist')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser and request.user.is_staff:
            form.base_fields = {k: v for k, v in form.base_fields.items() if k == 'is_verified'}
        return form

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser and request.user.is_staff:
            return hasattr(request.user, 'maintainer_profile') and request.user.maintainer_profile.is_verified
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class HotelStaffAdmin(admin.ModelAdmin):
    list_display = (
        'staff_id', 'user_link', 'department', 'hire_date', 'is_active_staff', 'hotel_gst_no', 
        'alternate_mobile_no', 'landline_no', 'shop_main_image_preview', 'shop_license_image_preview', 
        'shop_aadhar_image_preview', 'owner_pan_image_preview', 'owner_aadhar_image_preview'
    )
    list_editable = ('department', 'is_active_staff', 'hotel_gst_no', 'alternate_mobile_no', 'landline_no')
    list_filter = ('department', 'is_active_staff')
    search_fields = ('staff_id', 'user__username', 'hotel_gst_no')
    
    fieldsets = (
        (None, {'fields': ('user', 'staff_id', 'department', 'hotel_gst_no', 'alternate_mobile_no', 'landline_no')}),
        ('Status', {'fields': ('hire_date', 'is_active_staff')}),
        ('Images', {'fields': ('shop_main_image', 'shop_license_image', 'shop_aadhar_image', 'owner_pan_image', 'owner_aadhar_image')}),
    )
    readonly_fields = ('hire_date',)

    def user_link(self, obj):
        return format_html('<a href="{}">{}</a>', f'/admin/user/user/{obj.user.pk}/change/', obj.user.username)
    user_link.short_description = 'User'

    def shop_main_image_preview(self, obj):
        return format_html('<img src="{}" width="50" />', obj.shop_main_image.url) if obj.shop_main_image else "No Image"
    shop_main_image_preview.short_description = 'Shop Main Img'

    def shop_license_image_preview(self, obj):
        return format_html('<img src="{}" width="50" />', obj.shop_license_image.url) if obj.shop_license_image else "No Image"
    shop_license_image_preview.short_description = 'License Img'

    def shop_aadhar_image_preview(self, obj):
        return format_html('<img src="{}" width="50" />', obj.shop_aadhar_image.url) if obj.shop_aadhar_image else "No Image"
    shop_aadhar_image_preview.short_description = 'Shop Aadhar Img'

    def owner_pan_image_preview(self, obj):
        return format_html('<img src="{}" width="50" />', obj.owner_pan_image.url) if obj.owner_pan_image else "No Image"
    owner_pan_image_preview.short_description = 'Owner PAN Img'

    def owner_aadhar_image_preview(self, obj):
        return format_html('<img src="{}" width="50" />', obj.owner_aadhar_image.url) if obj.owner_aadhar_image else "No Image"
    owner_aadhar_image_preview.short_description = 'Owner Aadhar Img'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class MaintainerAdmin(admin.ModelAdmin):
    list_display = (
        'maintainer_id', 'user_link', 'name', 'phone_no', 'alternate_phone_no', 'designation',
        'hire_date', 'is_verified_link', 'profile_img_preview', 'aadhar_img_preview', 'pan_img_preview'
    )
    list_editable = ('name', 'phone_no', 'alternate_phone_no', 'designation')
    list_filter = ('is_verified', 'designation')
    search_fields = ('maintainer_id', 'user__username', 'name', 'phone_no')
    
    fieldsets = (
        (None, {'fields': ('user', 'maintainer_id', 'name', 'phone_no', 'alternate_phone_no', 'designation')}),
        ('Documents', {'fields': ('profile_img', 'aadhar_img', 'pan_img')}),
        ('Status', {'fields': ('hire_date', 'is_verified')}),
        ('Managed Users', {'fields': ('managed_users_list',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('hire_date', 'managed_users_list')

    def managed_users_list(self, obj):
        if not obj.is_verified:
            return "Maintainer must be verified to manage users."
        users = User.objects.exclude(maintainer_profile__isnull=False).order_by('username')
        user_list = []
        for user in users:
            status = "Verified" if user.is_verified else "Not Verified"
            toggle_url = f'/admin/user/user/{user.pk}/toggle_verified/'
            user_list.append(
                format_html('<li><a href="{}">{}</a> ({})</li>', toggle_url, user.username, status)
            )
        return format_html('<ul>{}</ul>', format_html(''.join(user_list))) if user_list else "No users to manage."
    managed_users_list.short_description = "Users & Hotel Staff"

    def user_link(self, obj):
        return format_html('<a href="{}">{}</a>', f'/admin/user/user/{obj.user.pk}/change/', obj.user.username)
    user_link.short_description = 'User'

    def is_verified_link(self, obj):
        status = "Verified" if obj.is_verified else "Not Verified"
        action = "Unverify" if obj.is_verified else "Verify"
        return format_html('<a href="{}">{}</a> ({})', f'/admin/user/maintainer/{obj.pk}/toggle_verified/', action, status)
    is_verified_link.short_description = 'Verification'

    def profile_img_preview(self, obj):
        return format_html('<img src="{}" width="50" />', obj.profile_img.url) if obj.profile_img else "No Image"
    profile_img_preview.short_description = 'Profile Img'

    def aadhar_img_preview(self, obj):
        return format_html('<img src="{}" width="50" />', obj.aadhar_img.url) if obj.aadhar_img else "No Image"
    aadhar_img_preview.short_description = 'Aadhar Img'

    def pan_img_preview(self, obj):
        return format_html('<img src="{}" width="50" />', obj.pan_img.url) if obj.pan_img else "No Image"
    pan_img_preview.short_description = 'PAN Img'

    actions = ['verify_maintainers', 'unverify_maintainers']

    def verify_maintainers(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, "Only superusers can verify maintainers.", level='error')
            return
        updated = 0
        for obj in queryset.filter(is_verified=False):
            obj.is_verified = True
            obj.user.is_verified = True
            obj.save()
            obj.user.save()
            updated += 1
        self.message_user(request, f"{updated} maintainers have been verified.")
    verify_maintainers.short_description = "Verify selected maintainers"

    def unverify_maintainers(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, "Only superusers can unverify maintainers.", level='error')
            return
        updated = 0
        for obj in queryset.filter(is_verified=True):
            obj.is_verified = False
            obj.user.is_verified = False
            obj.save()
            obj.user.save()
            updated += 1
        self.message_user(request, f"{updated} maintainers have been unverified.")
    unverify_maintainers.short_description = "Unverify selected maintainers"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:maintainer_id>/toggle_verified/', self.admin_site.admin_view(self.toggle_verified), name='toggle_verified'),
        ]
        return custom_urls + urls

    def toggle_verified(self, request, maintainer_id):
        if not request.user.is_superuser:
            self.message_user(request, "Only superusers can toggle maintainer verification.", level='error')
            return redirect('admin:user_maintainer_changelist')
        maintainer = self.get_object(request, maintainer_id)
        if maintainer:
            maintainer.is_verified = not maintainer.is_verified
            maintainer.user.is_verified = maintainer.is_verified
            maintainer.save()
            maintainer.user.save()
            self.message_user(request, f"Maintainer {maintainer.maintainer_id} verification status updated to {maintainer.is_verified}.")
        return redirect('admin:user_maintainer_changelist')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser and request.user.is_staff:
            if not hasattr(request.user, 'maintainer_profile') or not request.user.maintainer_profile.is_verified:
                form.base_fields = {}
            else:
                form.base_fields = {k: v for k, v in form.base_fields.items() if k == 'is_verified'}
        return form

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser and request.user.is_staff:
            return hasattr(request.user, 'maintainer_profile') and request.user.maintainer_profile.is_verified
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

# Register all models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(HotelStaff, HotelStaffAdmin)
admin.site.register(Maintainer, MaintainerAdmin)
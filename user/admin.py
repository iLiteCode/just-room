from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import redirect
from django.utils.html import format_html
from .models import User, HotelStaff

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
            'fields': ('username', 'name', 'phone', 'email', 'password1', 'password2', 'is_staff', 'is_verified', 'paid_member', 'profile_image', 'aadhar_image', 'pancard_image'),
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

class HotelStaffAdmin(admin.ModelAdmin):
    list_display = (
        'staff_id', 'user_link', 'department', 'hire_date', 'is_active_staff_link', 'hotel_gst_no',
        'alternate_mobile_no', 'landline_no', 'shop_main_image_preview', 'shop_license_image_preview',
        'shop_aadhar_image_preview', 'owner_pan_image_preview', 'owner_aadhar_image_preview'
    )
    list_editable = ('department', 'hotel_gst_no', 'alternate_mobile_no', 'landline_no')
    list_filter = ('department', 'is_active_staff')
    search_fields = ('staff_id', 'user__username')
    
    fieldsets = (
        (None, {'fields': ('user', 'staff_id', 'department')}),
        ('Contact Info', {'fields': ('alternate_mobile_no', 'landline_no')}),
        ('Business Details', {'fields': ('hotel_gst_no',)}),
        ('Documents', {'fields': ('shop_main_image', 'shop_license_image', 'shop_aadhar_image', 'owner_pan_image', 'owner_aadhar_image')}),
        ('Status', {'fields': ('hire_date', 'is_active_staff')}),
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def user_link(self, obj):
        return format_html('<a href="{}">{}</a>', f'/admin/user/user/{obj.user.pk}/change/', obj.user.username)
    user_link.short_description = 'User'

    def is_active_staff_link(self, obj):
        status = "Active" if obj.is_active_staff else "Inactive"
        action = "Deactivate" if obj.is_active_staff else "Activate"
        return format_html('<a href="{}">{}</a> ({})', f'/admin/user/hotelstaff/{obj.pk}/toggle_active_staff/', action, status)
    is_active_staff_link.short_description = 'Active Status'

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

    actions = ['activate_staff', 'deactivate_staff']

    def activate_staff(self, request, queryset):
        updated = queryset.filter(is_active_staff=False).update(is_active_staff=True)
        self.message_user(request, f"{updated} staff have been activated.")
    activate_staff.short_description = "Activate selected staff"

    def deactivate_staff(self, request, queryset):
        updated = queryset.filter(is_active_staff=True).update(is_active_staff=False)
        self.message_user(request, f"{updated} staff have been deactivated.")
    deactivate_staff.short_description = "Deactivate selected staff"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:staff_id>/toggle_active_staff/', self.admin_site.admin_view(self.toggle_active_staff), name='toggle_active_staff'),
        ]
        return custom_urls + urls

    def toggle_active_staff(self, request, staff_id):
        staff = self.get_object(request, staff_id)
        if staff:
            staff.is_active_staff = not staff.is_active_staff
            staff.save()
            self.message_user(request, f"Staff {staff.staff_id} active status updated to {staff.is_active_staff}.")
        return redirect('admin:user_hotelstaff_changelist')

admin.site.register(User, UserAdmin)
admin.site.register(HotelStaff, HotelStaffAdmin)
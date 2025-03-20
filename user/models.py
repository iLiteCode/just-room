from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=50, default='Users no name mentioned')
    phone = models.CharField(max_length=20, default='8888888888')
    paid_member = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='user_profiles/', null=True, blank=True)
    aadhar_image = models.ImageField(upload_to='user_aadhar/', null=True, blank=True)
    pancard_image = models.ImageField(upload_to='user_pancard/', null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True, help_text="The groups this user belongs to.")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set", blank=True, help_text="Specific permissions for this user.")

    def __str__(self):
        return self.username

class HotelStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='hotel_staff_profile')
    staff_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=50, choices=[('reception', 'Reception'), ('housekeeping', 'Housekeeping'), ('management', 'Management'), ('kitchen', 'Kitchen')], default='reception')
    hire_date = models.DateField(auto_now_add=True)
    is_active_staff = models.BooleanField(default=True)
    hotel_gst_no = models.CharField(max_length=15, null=True, blank=True)
    alternate_mobile_no = models.CharField(max_length=20, null=True, blank=True)
    landline_no = models.CharField(max_length=15, null=True, blank=True)
    shop_main_image = models.ImageField(upload_to='shop_main/', null=True, blank=True)
    shop_license_image = models.ImageField(upload_to='shop_licenses/', null=True, blank=True)
    shop_aadhar_image = models.ImageField(upload_to='shop_aadhar/', null=True, blank=True)
    owner_pan_image = models.ImageField(upload_to='owner_pancard/', null=True, blank=True)
    owner_aadhar_image = models.ImageField(upload_to='owner_aadhar/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Only set is_staff and initial verification status on creation, not updates
        if not self.pk:  # If this is a new instance
            self.user.is_staff = True
            self.user.is_verified = False  # Set only on creation
            self.is_active_staff = True    # Set only on creation
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.staff_id}"
    

class Maintainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='maintainer_profile')
    maintainer_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=20)
    alternate_phone_no = models.CharField(max_length=20, null=True, blank=True)
    is_verified = models.BooleanField(default=False)  # Verified by superuser
    hire_date = models.DateField(auto_now_add=True)
    designation = models.CharField(
        max_length=50,
        choices=[
            ('technician', 'Technician'),
            ('supervisor', 'Supervisor'),
            ('manager', 'Manager'),
            ('support', 'Support'),
        ],
        default='technician'
    )
    profile_img = models.ImageField(upload_to='maintainer_profiles/', null=True, blank=True)
    aadhar_img = models.ImageField(upload_to='maintainer_aadhar/', null=True, blank=True)
    pan_img = models.ImageField(upload_to='maintainer_pancard/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # If new instance
            self.user.is_staff = True
            self.user.is_verified = False
            self.is_verified = False
        # Sync is_verified with User model
        self.user.is_verified = self.is_verified
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.maintainer_id}"
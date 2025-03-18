from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Custom User model for all users (including regular users and hotel staff)
class User(AbstractUser):
    name = models.CharField(max_length=50, default='Default')  # Using 'name' instead of first_name
    phone = models.CharField(max_length=20, default='8888888888')
    paid_member = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # Custom field for email verification

    # Override groups and user_permissions to avoid conflicts with auth.User
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Custom related_name to avoid clash
        blank=True,
        help_text="The groups this user belongs to."
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Custom related_name to avoid clash
        blank=True,
        help_text="Specific permissions for this user."
    )

    def __str__(self):
        return self.username


# Hotel Staff model linked to the User model (one-to-one relationship)
class HotelStaff(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='hotel_staff_profile'
    )
    staff_id = models.CharField(max_length=10, unique=True)  # Unique staff identifier (e.g., "HSTF001")
    department = models.CharField(
        max_length=50,
        choices=[
            ('reception', 'Reception'),
            ('housekeeping', 'Housekeeping'),
            ('management', 'Management'),
            ('kitchen', 'Kitchen'),
        ],
        default='reception'
    )
    hire_date = models.DateField(auto_now_add=True)  # Date staff was added
    is_active_staff = models.BooleanField(default=True)  # Whether staff is currently active in the hotel

    def save(self, *args, **kwargs):
        # Ensure the linked User is marked as staff and saved
        self.user.is_staff = True
        self.user.is_active = False  # Inactive until email verification
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.staff_id}"
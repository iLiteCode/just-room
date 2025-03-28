# Generated by Django 5.1.5 on 2025-03-20 07:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_hotelstaff_alternate_mobile_no_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintainer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='maintainer_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('maintainer_id', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('phone_no', models.CharField(max_length=20)),
                ('alternate_phone_no', models.CharField(blank=True, max_length=20, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('hire_date', models.DateField(auto_now_add=True)),
                ('designation', models.CharField(choices=[('technician', 'Technician'), ('supervisor', 'Supervisor'), ('manager', 'Manager'), ('support', 'Support')], default='technician', max_length=50)),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to='maintainer_profiles/')),
                ('aadhar_img', models.ImageField(blank=True, null=True, upload_to='maintainer_aadhar/')),
                ('pan_img', models.ImageField(blank=True, null=True, upload_to='maintainer_pancard/')),
            ],
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-09 20:24

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0009_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(default='profiles/ca7ecpl0mbnn27xk5se6.jpg', max_length=255, verbose_name='image'),
        ),
    ]
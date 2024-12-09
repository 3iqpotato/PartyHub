# Generated by Django 5.1.3 on 2024-12-03 23:46

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(default='profiles/default_img_d3fjl6.jpg', max_length=255, verbose_name='image'),
        ),
    ]
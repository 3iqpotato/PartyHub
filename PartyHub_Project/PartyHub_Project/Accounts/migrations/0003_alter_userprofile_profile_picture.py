# Generated by Django 5.1.3 on 2024-11-13 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_remove_userprofile_is_vip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='images/profiles/default_img.jpg', null=True, upload_to='profiles/'),
        ),
    ]

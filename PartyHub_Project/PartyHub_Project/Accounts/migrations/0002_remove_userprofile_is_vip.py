# Generated by Django 5.1.3 on 2024-11-11 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_vip',
        ),
    ]

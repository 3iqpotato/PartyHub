# Generated by Django 5.1.3 on 2024-11-11 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ticket', '0002_rename_event_ticket_party'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]

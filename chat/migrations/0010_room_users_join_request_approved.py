# Generated by Django 4.0.6 on 2022-08-18 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_remove_message_room_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='room_users',
            name='join_request_approved',
            field=models.BooleanField(null=True),
        ),
    ]

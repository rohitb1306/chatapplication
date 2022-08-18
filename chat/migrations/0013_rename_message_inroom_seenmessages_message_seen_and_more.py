# Generated by Django 4.0.6 on 2022-08-18 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_remove_message_number_of_views_seenmessages'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seenmessages',
            old_name='message_inroom',
            new_name='message_seen',
        ),
        migrations.AddField(
            model_name='seenmessages',
            name='message_in_room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.room'),
        ),
    ]

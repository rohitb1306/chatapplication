from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=255)
    is_private_group = models.BooleanField(default=False)
    is_single_user = models.BooleanField(default=False)
    # from_user=models.CharField(max_length=50,null=True)
    # hi=models.CharField(max_length=10)
    # to_user=models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name


class Room_users(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    join_request_approved=models.BooleanField(null=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    chat_message = RichTextField(null=True)
    message_arrival_time = models.DateTimeField(auto_now_add=True)
    message_seen = models.BooleanField(default=False)
    room_name = models.ForeignKey(Room, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)


class SeenMessages(models.Model):
    message_seen=models.ForeignKey(Message,on_delete=models.CASCADE)
    users_in_room=models.ForeignKey(Room_users,on_delete=models.CASCADE)
    message_in_room=models.ForeignKey(Room,on_delete=models.CASCADE)

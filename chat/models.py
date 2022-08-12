from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.

class Room(models.Model):
    name=models.CharField(max_length=255)
    is_private=models.BooleanField(default=False)
    is_single_user=models.BooleanField(default=False)
    from_user=models.CharField(max_length=50,null=True)
    hi=models.CharField(max_length=10)
    to_user=models.CharField(max_length=50,null=True)
    room_password=models.CharField(null=True,max_length=50)

    def __str__(self):
        return self.name

class Message(models.Model):

    chat_message=RichTextField(null=True)
    message_arrival_time=models.DateTimeField(auto_now=True)

    room_name=models.ForeignKey(Room,on_delete=models.CASCADE)
    from_user=models.ForeignKey(User,on_delete=models.CASCADE)

    

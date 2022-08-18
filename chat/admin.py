from email import message
from django.contrib import admin
from .models import Message, Room, Room_users, SeenMessages

# Register your models here.
@admin.register(Message)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "from_user",
        "room_name",
        "message_arrival_time",
        "chat_message",
    ]
    list_per_page = 15


@admin.register(Room)
class RoomModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(Room_users)
admin.site.register(SeenMessages)

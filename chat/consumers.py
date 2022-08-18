import json
from channels.generic.websocket import (
    AsyncWebsocketConsumer,
)  # ,WebsocketConsumer

# from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Message, Room, Room_users, SeenMessages
import pdb

# from cgitb import text


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name=self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name='chat_%s' % self.room_name
#         #connection of the room
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         #disconnection or leaving the room
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     #receive message from websocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         user= text_data_json['user']
#         room=Room.objects.get(name=text_data_json['roomName'])
#         user1=User.objects.get(username=user)
#         msg=Message(
#                 chat_message=message,
#                 room_name=room,
#                 from_user=user1
#                 )
#         msg.save()
#         #send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type':'chat_message',
#                 'message':message,
#                 'user':user,
#             }
#         )
# # receveing message from group
#     def chat_message(self,event):
#         message=event['message']
#         user=event['user']
#         #sending message to websocket
#         self.send(text_data=json.dumps({
#             'message': message,
#             'user':user
#         }))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"][
            "room_name"
        ]
        self.room_group_name = "chat_%s" % self.room_name
        # room=await database_sync_to_async(Room.objects.get)(name=self.room_name)

        # messg=await database_sync_to_async(Message.objects.get)(message_seen=False)
        # print(messg)
        # pdb.set_trace()
        # await print(room)
        # for i in messg:
        #     print(i)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json["message"]
        user = self.scope["user"].username
        room = await database_sync_to_async(Room.objects.get)(
            name=text_data_json["roomName"]
        )
        user1 = await database_sync_to_async(User.objects.get)(
            username=user
        )
        msg = Message(
            chat_message=message,
            room_name=room,
            from_user=user1,
        )
        await database_sync_to_async(msg.save)()
        msg=await database_sync_to_async(Message.objects.get)(chat_message=message,room_name=room,message_seen=False)
        room_user=await database_sync_to_async(Room_users.objects.get)(room=room,user=user1)
        msg_seen=SeenMessages(
            message_seen=msg,
            users_in_room=room_user,
            message_in_room=room
        )
        await database_sync_to_async(msg_seen.save)()
        # message=await database_sync_to_async(Message.objects.get)(from_user=user1)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": user,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        await self.send(
            text_data=json.dumps({"message": message, "user": user})
        )

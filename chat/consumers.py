
import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from . models import Message,Room

from cgitb import text


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
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        message = text_data_json['message']
        user=text_data_json['user']

        room=await database_sync_to_async(Room.objects.get)(name=text_data_json['roomName'])
        user1=await database_sync_to_async(User.objects.get)(username=user)
        msg=Message(
                chat_message=message,
                room_name=room,
                from_user=user1
                )
        await database_sync_to_async(msg.save)()
        print(text_data_json)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        # await print(Message.objects.all())
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message, 
            'user': user
        }))
    
    
        

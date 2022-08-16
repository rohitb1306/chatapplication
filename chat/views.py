
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View

from chat.models import Message, Room
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import chatform
# Create your views here.


class ChatIndex(TemplateView):
    template_name='chat/index.html'

class Rooms(View):
    
    def get(self,request,room_name):
        room1=Room.objects.filter(name=room_name).first()
        if room1.is_single_user:
            if request.user.username==room1.from_user or request.user.username==room1.to_user:
                
                message=Message.objects.filter(room_name=room1).order_by('message_arrival_time')
                return render(request, 'chat/room.html', {
                            'room_name': room_name,'messages1':message,'form':chatform,'room':room1
                        })
            else:
                messages.warning(request,"cannot see others personal message")
                return redirect('/')
        else:
            message=Message.objects.filter(room_name=room1).order_by('message_arrival_time')
            return render(request, 'chat/room.html', {
                            'room_name': room_name,'messages1':message,'form':chatform,'room':room1
                        })

class Room1(View):
    def get(self,request,room_name):
        if request.user.is_authenticated:
            return redirect('room',room_name)
        else:
            messages.warning(request,'plzz login')
            return redirect('login')       

class Room2(View):
    def get(self,request):
        chat_name=request.GET['room-name']
        chat_type=request.GET['room-type']
        room1=Room.objects.filter(name=chat_name).first()
        if room1:
            if chat_type=='private':
                password=request.GET['password']
                if room1.room_password==password:
                    return redirect('room',chat_name)
                else:
                    messages.warning(request,'wrong password for the existing room')
            elif chat_type=='public':
                return redirect('room',chat_name) 
        elif User.objects.filter(username=chat_name).exists():
            if Room.objects.filter(from_user=request.user.username,to_user=chat_name): 
                return redirect('room',Room.objects.get(from_user=request.user.username,to_user=chat_name).name)
            elif Room.objects.filter(from_user=chat_name,to_user=request.user.username):
                return redirect('room',Room.objects.get(from_user=chat_name,to_user=request.user.username).name)
            else:
                room_name=request.user.username+chat_name
                room=Room(name=room_name,is_single_user=True,from_user=request.user.username,to_user=chat_name)
                room.save()
                messages.success(request,f"{room_name}")
                return redirect('room',room_name)

        else:
            if chat_type=='private':
                password=request.GET['password']
                room=Room(name=chat_name,is_private=True,room_password=password,from_user=request.user.username)
                room.save()
                return redirect('room',chat_name)
            elif chat_type=='public':
                room=Room(name=chat_name,from_user=request.user.username)
                room.save()
                return redirect('room',chat_name)
            else:
                messages.warning(request,"no user with that username")
                return redirect('chatindex')
    

# def room(request, room_name):
#     # save_message(room_name)
#     messages=[]
#     room1=Room.objects.filter(name=room_name).first()
#     if room1:
#         messages=Message.objects.filter(room_name=room1)
#         return render(request, 'chat/room.html', {
#                 'room_name': room_name,'messages1':messages
#             })
#     else:
#         room=Room(name=room_name)
#         room.save()
#         return render(request,'chat/room.html', {
#                 'room_name': room_name,'messages1':messages
#             })
    
class Deleteroom(View):
    def get(self,request,room_id):
        room=Room.objects.get(id=room_id)
        if request.user.username==room.from_user or request.user.username==room.to_user:
            room.delete()
            messages.success(request,'room deleted')
            return redirect('/')
        else:
            messages.warning(request,'you dont have permision to delete this room')
            return redirect('/')


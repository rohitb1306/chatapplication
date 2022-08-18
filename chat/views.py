from argparse import RawDescriptionHelpFormatter
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View

from chat.models import Message, Room, Room_users, SeenMessages
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import chatform
from django.shortcuts import get_object_or_404

# Create your views here.


class ChatIndex(TemplateView):
    template_name = "chat/index.html"


class Rooms(View):
    def get(self, request, room_name):
        room1 = Room.objects.filter(name=room_name).first()
        if room1.is_single_user:
            room2 = Room.objects.get(
                name=room_name, is_single_user=True
            )
            room_user_obj = Room_users.objects.filter(
                room=room2, user=request.user
            )
            if room_user_obj:
                message = Message.objects.filter(
                    room_name=room2
                ).order_by("message_arrival_time")
                room_user_admin = Room_users.objects.filter(
                    room=room2
                )
                all_users_inroom = Room_users.objects.filter(
                    room=room2
                )
                for i in message:
                    if request.user != i.from_user:
                        i.message_seen = True
                        i.save()
                    # print(request.user,i.from_user)
                return render(
                    request,
                    "chat/room.html",
                    {
                        "room_name": room_name,
                        "messages1": message,
                        "form": chatform,
                        "room": room2,
                        "room_user": room_user_admin,
                        "all_user_inroom": all_users_inroom,
                    },
                )
            else:
                messages.warning(
                    request, "cannot see others personal message"
                )
                return redirect("/")
        elif room1.is_private_group:
            room2 = Room.objects.get(
                name=room_name, is_private_group=True
            )
            room_user_obj = Room_users.objects.filter(
                room=room2, user=request.user
            )
            if room_user_obj:
                message = Message.objects.filter(
                    room_name=room2
                ).order_by("message_arrival_time")
                room_user_admin = Room_users.objects.get(
                    room=room2, is_admin=True
                )
                all_users_inroom = Room_users.objects.filter(
                    room=room2
                )
                # print(len(all_users_inroom))
                for i in message:
                    room_user=Room_users.objects.filter(room=room2,user=request.user).first()
                    msg_seen=SeenMessages.objects.filter(message_seen=i,message_in_room=room2)
                    room_users=Room_users.objects.filter(room=room2)
                    # print(room_user)
                    # print(SeenMessages.objects.filter(message_seen=i,message_in_room=room2,users_in_room=room_user),i)
                    if SeenMessages.objects.filter(message_seen=i,message_in_room=room2,users_in_room=room_user):
                        if len(msg_seen) == len(room_users):
                            i.message_seen = True
                            i.save()
                    else:
                        msg_seen1=SeenMessages(
                            message_seen=i,
                            users_in_room=room_user,
                            message_in_room=room2
                        )
                        msg_seen1.save()
                return render(
                    request,
                    "chat/room.html",
                    {
                        "room_name": room_name,
                        "messages1": message,
                        "form": chatform,
                        "room": room2,
                        "room_user": room_user_admin,
                        "all_users_inroom": all_users_inroom,
                    },
                )
            else:
                messages.warning(
                    request, "cannot see others personal message"
                )
                return redirect("/")
        else:
            room2 = Room.objects.get(
                name=room_name,
                is_private_group=False,
                is_single_user=False,
            )
            message = Message.objects.filter(
                room_name=room2
            ).order_by("message_arrival_time")
            room_user_admin = Room_users.objects.get(
                room=room2, is_admin=True
            )
            all_users_inroom = Room_users.objects.filter(room=room2,join_request_approved=True)
            lst=[]
            for i in all_users_inroom:
                lst.append(i.user.username)
            user_approval=Room_users.objects.filter(room=room2,join_request_approved=False)

            for i in message:
                    room_user=Room_users.objects.filter(room=room2,user=request.user).first()
                    msg_seen=SeenMessages.objects.filter(message_seen=i,message_in_room=room2)
                    room_users=Room_users.objects.filter(room=room2)
                    # print(room_user)
                    # print(SeenMessages.objects.filter(message_seen=i,message_in_room=room2,users_in_room=room_user),i)
                    if SeenMessages.objects.filter(message_seen=i,message_in_room=room2,users_in_room=room_user):
                        if len(msg_seen) == len(room_users):
                            i.message_seen = True
                            i.save()
                    else:
                        msg_seen1=SeenMessages(
                            message_seen=i,
                            users_in_room=room_user,
                            message_in_room=room2
                        )
                        msg_seen1.save()
            return render(
                request,
                "chat/room.html",
                {
                    "room_name": room_name,
                    "messages1": message,
                    "form": chatform,
                    "room": room1,
                    "room_user": room_user_admin,
                    "all_users_inroom": lst,
                    "user_approval":user_approval
                },
            )


class Room1(View):
    def get(self, request, room_name):
        if request.user.is_authenticated:
            return redirect("room", room_name)

        else:
            messages.warning(request, "plzz login")
            return redirect("login")


class Room2(View):
    def get(self, request):
        chat_name = request.GET["room-name"]
        chat_type = request.GET["room-type"]
        room1 = Room.objects.filter(name=chat_name).first()
        if room1:
            return redirect("room", chat_name)
        elif User.objects.filter(username=chat_name).exists():
            if Room.objects.filter(
                name=(request.user.username + chat_name)
            ):
                return redirect(
                    "room",
                    Room.objects.get(
                        name=(request.user.username + chat_name)
                    ).name,
                )
            elif Room.objects.filter(
                name=(chat_name + request.user.username)
            ):
                return redirect(
                    "room",
                    Room.objects.get(
                        name=(chat_name + request.user.username)
                    ).name,
                )

            else:
                room_name = request.user.username + chat_name
                room = Room(name=room_name, is_single_user=True)
                room.save()
                room1 = Room.objects.get(name=room_name)
                print(room1)
                room_user_object = Room_users(
                    room=room1, user=request.user, is_admin=True
                )
                room_user_object.save()
                room_user_object = Room_users(
                    room=room1,
                    user=User.objects.get(username=chat_name),
                    is_admin=True,
                )
                room_user_object.save()
                messages.success(request, f"{room_name}")
                return redirect("room", room_name)

        else:
            if chat_type == "private":
                room = Room(name=chat_name, is_private_group=True)
                room.save()
                room = Room.objects.get(name=chat_name)
                user_in_room = Room_users(
                    room=room, user=request.user, is_admin=True
                )
                user_in_room.save()
                return redirect("room", chat_name)
            elif chat_type == "public":
                room = Room(name=chat_name)
                room.save()
                room = Room.objects.get(name=chat_name)
                user_in_room = Room_users(
                    room=room, user=request.user, is_admin=True
                )
                user_in_room.save()
                return redirect("room", chat_name)
            else:
                messages.warning(
                    request, "no user with that username"
                )
                return redirect("chatindex")


class Deleteroom(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        room_user_obj = Room_users.objects.filter(
            is_admin=True, room=room
        )
        if request.user in room_user_obj:
            room.delete()
            messages.success(request, "room deleted")
            return redirect("/")
        else:
            messages.warning(
                request, "you dont have permision to delete this room"
            )
            return redirect("/")


class Addmember(View):
    def post(self, request, room_id):
        user_str = request.POST["userlist"]
        # user_list=user_str.split(',')
        return redirect("add-member", room_id, user_str)


class Addmember1(View):
    def get(self, request, room_id, str):
        room_obj = Room.objects.get(id=room_id)
        room_user_obj = Room_users.objects.filter(
            room=room_obj, user=request.user, is_admin=True
        )
        if room_user_obj:
            for user in str.split(","):

                user_obj = User.objects.get(username=user)
                room_user = Room_users(room=room_obj, user=user_obj)
                room_user.save()
            messages.success(request, "added users to room")
            return redirect("room", room_obj.name)
        else:
            return redirect("room", room_obj.name)


class Deletemember(View):
    def post(self, request, room_id):
        user_str = request.POST["userlist"]
        room_obj = Room.objects.get(id=room_id)
        room_user_obj = Room_users.objects.filter(
            room=room_obj, user=request.user, is_admin=True
        )
        if room_user_obj:
            for user in user_str.split(","):
                user_obj = User.objects.get(username=user)
                room_user_toremove = Room_users.objects.get(
                    user=user_obj, room=room_obj
                )
                room_user_toremove.delete()
                messages.success(request, "removed user")
                return redirect("room", room_obj.name)
        else:
            return redirect("room", room_obj.name)

class Joinrequest(View):
    def get(self,request,room_id):
        room=Room.objects.get(id=room_id)
        room_user_object=Room_users(room=room,user=request.user,join_request_approved=False)
        room_user_object.save()
        messages.success(request,'joined the room waiting for room admin approval')
        return redirect('/')
    
class Approverequest(View):
    def get(self,request,room_id,user_id):
        room=Room.objects.get(id=room_id)
        user_obj=User.objects.get(id=user_id)
        room_user_object=Room_users.objects.get(room=room,user=user_obj)
        room_user_object.join_request_approved=True
        room_user_object.save()
        return redirect('room',room.name)
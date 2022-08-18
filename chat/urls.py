from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatIndex.as_view(), name="chatindex"),
    path("room/<str:room_name>/", views.Rooms.as_view(), name="room"),
    path(
        "room1/<str:room_name>/", views.Room1.as_view(), name="room1"
    ),
    path("room2", views.Room2.as_view(), name="room2"),
    path(
        "deleteroom/<room_id>",
        views.Deleteroom.as_view(),
        name="deleteroom",
    ),
    path(
        "add-member-select/<room_id>",
        views.Addmember.as_view(),
        name="add-member-select",
    ),
    path(
        "delete-member-select/<room_id>",
        views.Deletemember.as_view(),
        name="delete-member-select",
    ),
    path(
        "add-member/<room_id>/<str>",
        views.Addmember1.as_view(),
        name="add-member",
    ),
    path(
        "public-room-join-request/<room_id>",
        views.Joinrequest.as_view(),
        name="public-room-join-request"
    ),
    path(
        "public-room-approve-request/<room_id>/<user_id>",
        views.Approverequest.as_view(),
        name="public-room-approve-request"
    )
]

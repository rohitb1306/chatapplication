from django.urls import path
from . import views
urlpatterns = [
    path('',views.ChatIndex.as_view(),name='chatindex'),
    path('room/<str:room_name>/', views.Rooms.as_view(), name='room'),
    path('room1/<str:room_name>/', views.Room1.as_view(), name='room1'),
    path('room2', views.Room2.as_view(), name='room2'),
    path('deleteroom/<room_id>', views.Deleteroom.as_view(), name='deleteroom'),
    ]
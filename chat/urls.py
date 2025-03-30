from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='home'),
    path('rooms/', views.chat_rooms, name='rooms'),
    path('rooms/create/', views.create_room, name='create_room'),
    path('<slug:room_slug>/', views.chat_room, name='room'),
    path('<slug:room_slug>/messages/', views.room_messages, name='room_messages'),
    path('<slug:room_slug>/participants/', views.room_participants, name='room_participants'),
    path('api/rooms/', views.api_rooms, name='api_rooms'),
    path('api/messages/<slug:room_slug>/', views.api_messages, name='api_messages'),
    path('api/notifications/', views.api_notifications, name='api_notifications'),
]
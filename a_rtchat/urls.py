from django.urls import URLPattern, path

from . import views

urlpatterns: list[URLPattern] = [
    path("", views.ChatView.as_view(), name="chat"),
    path("chat/room/<chatroom_name>", views.ChatView.as_view(), name="private-chat"),
    path(
        "chat/start/<username>", views.GetOrCreateChatRoom.as_view(), name="start-chat"
    ),
]

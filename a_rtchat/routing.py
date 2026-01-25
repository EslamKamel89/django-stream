from django.urls import URLPattern, path

from . import consumers

websocket_urlpatterns = [
    path("ws/chatroom/<chatroom_name>", consumers.ChatRoomConsumer.as_asgi()),  # type: ignore
]

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from a_rtchat.forms import GroupMessageCreateForm
from a_rtchat.models import ChatGroup, GroupMessage
from a_rtchat.types import MessageResponse


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = f"chat-{self.get_room_name()}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code: int) -> None:
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        return super().disconnect(code)

    def receive(
        self,
        text_data: str | None = None,
        bytes_data: bytes | None = None,
    ) -> None:
        if not text_data:
            return
        chat_group = self.get_chat_group()
        try:
            data = json.loads(text_data)
        except Exception as e:
            return
        form = GroupMessageCreateForm(data=data)
        if not form.is_valid():
            self.send(
                json.dumps(
                    {
                        "ok": False,
                        "errors": form.errors,
                    }
                )
            )
            return
        message: GroupMessage = form.save(commit=False)
        message.author = self.scope.get("user")
        message.group = chat_group
        message.save()
        message_response: MessageResponse = {
            "id": message.id,
            "body": message.body,
            "author": {
                "id": message.author.id,  # type: ignore
                "username": message.author.username,  # type: ignore
                "avatar": message.author.profile.avatar_url,  # type: ignore
            },
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message_response,
            },
        )

    def chat_message(self, event):
        self.send(json.dumps({"ok": True, "message": event["message"]}))

    def get_room_name(self) -> str:
        return self.scope["url_route"]["kwargs"]["chatroom_name"]  # type: ignore

    def get_chat_group(self) -> ChatGroup | None:
        chat_group = ChatGroup.objects.filter(group_name=self.get_room_name()).first()
        return chat_group

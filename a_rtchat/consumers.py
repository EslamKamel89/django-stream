import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from a_rtchat.forms import GroupMessageCreateForm
from a_rtchat.models import ChatGroup, GroupMessage
from a_rtchat.types import MessageResponse


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = f"chat-{self.get_room_name()}"
        self.user: User = self.scope.get("user")  # type: ignore
        if not self.user.is_authenticated:
            self.close()
            return
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        chat_group: ChatGroup = self.get_chat_group()

        self.chat_group = chat_group
        if (
            self.chat_group
            and not self.chat_group.users_online.filter(id=self.user.id).exists()  # type: ignore
        ):
            self.chat_group.users_online.add(self.user)
            self.update_online_count()
        self.accept()

    def disconnect(self, code: int) -> None:
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        chat_group = self.chat_group
        if chat_group and self.chat_group.users_online.filter(id=self.user.id).exists():  # type: ignore
            chat_group.users_online.remove(self.user)
            self.update_online_count()
        return super().disconnect(code)

    def receive(
        self,
        text_data: str | None = None,
        bytes_data: bytes | None = None,
    ) -> None:
        if not text_data:
            return
        chat_group = self.chat_group
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
        message.author = self.user
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
                "type": "chat_message_handler",
                "message": message_response,
            },
        )

    def chat_message_handler(self, event):
        self.send(
            json.dumps({"ok": True, "message": event["message"], "event": "message"})
        )

    def get_room_name(self) -> str:
        return self.scope["url_route"]["kwargs"]["chatroom_name"]  # type: ignore

    def get_chat_group(self) -> ChatGroup:
        chat_group_name = self.get_room_name()
        chat_group = ChatGroup.objects.filter(group_name=chat_group_name).first()
        if not chat_group:
            raise RuntimeError(f"Chat Group: {chat_group_name} not found")
        return chat_group

    def update_online_count(self):
        online_count = self.chat_group.users_online.count()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "online_count_handler",
                "online_count": online_count,
            },
        )

    def online_count_handler(self, event):
        self.send(
            json.dumps(
                {
                    "ok": True,
                    "online_count": event["online_count"],
                    "event": "online_count",
                }
            )
        )

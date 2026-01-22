import json
from http.client import HTTPException

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from a_rtchat.forms import GroupMessageCreateForm

from .models import *


class ChatView(LoginRequiredMixin, View):
    def get_chat_group(self) -> ChatGroup:
        chat_group = get_object_or_404(ChatGroup, group_name="Django")
        return chat_group

    def get_chat_messages(self, chat_group: ChatGroup) -> QuerySet[GroupMessage]:
        chat_messages = chat_group.chat_messages.all()[:30]
        return chat_messages

    def get(self, request: HttpRequest):
        chat_group = self.get_chat_group()
        messages = self.get_chat_messages(chat_group)
        serialized_messages = [
            {
                "id": msg.id,
                "body": msg.body,
                "author": {
                    "username": msg.author.username,
                    "avatar": msg.author.profile.avatar_url,  # type: ignore
                },
                "is_me": msg.author == request.user,
            }
            for msg in reversed(messages)
        ]
        return render(
            request,
            "a_rtchat/chat.html",
            {
                "chat_group": chat_group,
                "serialized_messages": serialized_messages,
            },
        )

    def post(self, request: HttpRequest):
        chat_group = self.get_chat_group()
        try:
            data = json.loads(request.body)
        except Exception as e:
            return HttpResponseBadRequest("Invalid json")
        form = GroupMessageCreateForm(data=data)
        if not form.is_valid():
            return JsonResponse(
                {
                    "ok": False,
                    "errors": form.errors,
                },
                status=400,
            )
        message: GroupMessage = form.save(commit=False)
        message.author = request.user  # type: ignore
        message.group = chat_group
        message.save()
        return JsonResponse(
            {
                "ok": True,
                "message": {
                    "id": message.id,
                    "body": message.body,
                    "author": {
                        "username": message.author.username,
                        "avatar": message.author.profile.avatar_url,  # type: ignore
                    },
                    "is_me": True,
                },
            }
        )

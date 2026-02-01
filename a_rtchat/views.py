import json
from http.client import HTTPException
from typing import Sequence

from django.contrib import messages as session_messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from a_rtchat.forms import GroupMessageCreateForm
from a_rtchat.types import MessageResponse

from .models import *


class ChatView(LoginRequiredMixin, View):
    def get_chat_group(self, chat_group_name: str | None = None) -> ChatGroup:
        chat_group = get_object_or_404(
            ChatGroup,
            group_name=chat_group_name or "django",
        )
        return chat_group

    def get_chat_messages(self, chat_group: ChatGroup) -> QuerySet[GroupMessage]:
        chat_messages = chat_group.chat_messages.all()[:30]  # type: ignore
        return chat_messages

    def get(self, request: HttpRequest, chatroom_name: str | None = None):
        chat_group = self.get_chat_group(chatroom_name)
        user: User = request.user  # type: ignore
        if chat_group.is_private and not chat_group.members.filter(id=user.id).exists():  # type: ignore
            session_messages.error(
                request, "You are not allowed to join this private chat"
            )
            return redirect(reverse("home"))
        messages = self.get_chat_messages(chat_group)
        serialized_messages: list[MessageResponse] = [
            {
                "id": msg.id,
                "body": msg.body,
                "author": {
                    "id": msg.author.id,
                    "username": msg.author.username,
                    "avatar": msg.author.profile.avatar_url,  # type: ignore
                },
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

    def post(self, request: HttpRequest, chatroom_name: str | None = None):
        chat_group = self.get_chat_group(chatroom_name)
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
        message_response: MessageResponse = {
            "id": message.id,
            "body": message.body,
            "author": {
                "id": message.author.id,  # type: ignore
                "username": message.author.username,  # type: ignore
                "avatar": message.author.profile.avatar_url,  # type: ignore
            },
        }
        return JsonResponse(
            {
                "ok": True,
                "message": message_response,
            }
        )


class GetOrCreateChatRoom(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, username: str):

        user: User = request.user  # type: ignore
        if username == user.username:
            session_messages.error(request, "You can't chat in private with yourself")
            return redirect(reverse("home"))

        other_user = get_object_or_404(User, username=username)
        private_chat_group: ChatGroup | None = (
            ChatGroup.objects.filter(is_private=True)
            .filter(members=user)
            .filter(members=other_user)
            .annotate(member_count=Count("members"))
            .filter(member_count=2)
            .first()
        )
        # my_chat_groups: QuerySet[ChatGroup] = request.user.chat_groups.filter(is_private=True)  # type: ignore

        # if my_chat_groups.exists():
        #     for chat_group in my_chat_groups:
        #         if chat_group.members.filter(id=other_user.id).exists():  # type: ignore
        #             private_chat_group = chat_group
        #             break
        if not private_chat_group:
            private_chat_group = ChatGroup.objects.create(is_private=True)
            private_chat_group.members.add(user, other_user)

        return redirect(reverse("private-chat", args=[private_chat_group.group_name]))

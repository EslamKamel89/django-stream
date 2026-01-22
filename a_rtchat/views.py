from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest
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
        chat_messages = self.get_chat_messages(chat_group)
        form = GroupMessageCreateForm()
        return render(
            request,
            "a_rtchat/chat.html",
            {"chat_group": chat_group, "chat_messages": chat_messages, "form": form},
        )

    def post(self, request: HttpRequest):
        chat_group = self.get_chat_group()
        form = GroupMessageCreateForm(data=request.POST)
        if form.is_valid():
            message_obj: GroupMessage = form.save(commit=False)
            message_obj.author = request.user  # type: ignore
            message_obj.group = chat_group
            message_obj.save()
            form = GroupMessageCreateForm()
        else:
            body_error = form.errors.get("body")
            if body_error and body_error[0]:
                messages.error(request, str(body_error[0]))
        chat_messages = self.get_chat_messages(chat_group)
        return render(
            request,
            "a_rtchat/chat.html",
            {"chat_group": chat_group, "chat_messages": chat_messages, "form": form},
        )

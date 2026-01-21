from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views import View

from a_rtchat.forms import GroupMessageCreateForm

from .models import *


class ChatView(LoginRequiredMixin, View):
    def get_chat_data(self):
        chat_group = get_object_or_404(ChatGroup, group_name="Django")
        chat_messages = chat_group.chat_messages.all()[:30]
        return (chat_group, chat_messages)

    def get(self, request: HttpRequest):
        chat_group, chat_messages = self.get_chat_data()
        form = GroupMessageCreateForm()
        return render(
            request,
            "a_rtchat/chat.html",
            {"chat_group": chat_group, "chat_messages": chat_messages, "form": form},
        )

    def post(self, request: HttpRequest):
        chat_group, chat_messages = self.get_chat_data()
        form = GroupMessageCreateForm(data=request.POST)
        if form.is_valid():
            message_obj: GroupMessage = form.save(commit=False)
            message_obj.author = request.user  # type: ignore
            message_obj.group = chat_group
            message_obj.save()
            form.data = {}
        return render(
            request,
            "a_rtchat/chat.html",
            {"chat_group": chat_group, "chat_messages": chat_messages, "form": form},
        )

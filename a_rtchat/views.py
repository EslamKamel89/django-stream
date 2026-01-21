from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views import View

from .models import *


class ChatView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        chat_group = get_object_or_404(ChatGroup, group_name="Django")
        chat_messages = chat_group.chat_messages.all()[:30]
        return render(
            request,
            "a_rtchat/chat.html",
            {"chat_group": chat_group, "chat_messages": chat_messages},
        )

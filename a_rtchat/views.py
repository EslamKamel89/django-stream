from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class ChatView(View):
    def get(self, request: HttpRequest):
        return render(request, "a_rtchat/chat.html")

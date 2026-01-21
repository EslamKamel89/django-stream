from django.contrib import admin

import a_rtchat.models as chat_models


@admin.register(chat_models.GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin): ...


@admin.register(chat_models.ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin): ...

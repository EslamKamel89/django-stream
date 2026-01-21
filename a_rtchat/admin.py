from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest

import a_rtchat.models as chat_models


@admin.register(chat_models.ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "group_name", "message_count")
    search_fields = ("group_name",)
    ordering = ("group_name",)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return (
            super()
            .get_queryset(request)
            .annotate(messages_count=Count("chat_messages"))
        )

    @admin.display(description="Messages Count")
    def message_count(self, obj: chat_models.ChatGroup) -> int:
        return obj.messages_count  # type: ignore


@admin.register(chat_models.GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "group", "short_body", "created_at")
    list_filter = ("group", "author", "created_at")
    search_fields = ("body", "author__username", "group__group_name")
    ordering = ("-created_at",)
    list_select_related = ("author", "group")

    @admin.display(description="Message content")
    def short_body(self, obj: chat_models.GroupMessage) -> str:
        return obj.body[:50] + ("…" if len(obj.body) > 50 else "")

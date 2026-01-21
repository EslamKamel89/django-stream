from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.db import models

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class ChatGroup(models.Model):
    id: int
    group_name = models.CharField(max_length=128, unique=True)
    chat_messages: "RelatedManager[GroupMessage]"

    def __str__(self) -> str:
        return self.group_name


class GroupMessageManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related("group", "author")


class GroupMessage(models.Model):
    id: int
    group = models.ForeignKey(
        ChatGroup, related_name="chat_messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, related_name="chat_messages", on_delete=models.CASCADE
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = GroupMessageManager()

    def __str__(self) -> str:
        return f"{self.author.username} : {self.body}"

    class Meta:
        ordering = ("-created_at",)

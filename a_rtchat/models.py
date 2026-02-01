from __future__ import annotations

from typing import TYPE_CHECKING

import shortuuid
from django.contrib.auth.models import User
from django.db import models


class ChatGroup(models.Model):
    id: int
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    users_online = models.ManyToManyField(
        User, related_name="online_in_groups", blank=True
    )
    members = models.ManyToManyField(
        User,
        related_name="chat_groups",
        blank=True,
    )
    is_private = models.BooleanField(default=False)

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

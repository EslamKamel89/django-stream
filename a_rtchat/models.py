from django.db import models


class ChatGroup(models.Model):
    id: int
    group_name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.group_name

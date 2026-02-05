from typing import cast

from django.contrib.auth.models import User
from django.http import HttpRequest

from .queries import get_private_chats_for_user
from .serializers import serialize_chat_list


def chats_processor(request: HttpRequest):
    user = cast(User, request.user)

    if not user.is_authenticated:
        return {"groups": []}

    groups = get_private_chats_for_user(user)
    return {"groups": serialize_chat_list(user, groups)}

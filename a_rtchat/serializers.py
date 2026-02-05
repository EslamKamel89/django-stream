from typing import NotRequired, Sequence, TypedDict, cast

from django.contrib.auth.models import User
from django.db.models import QuerySet

from a_rtchat.models import ChatGroup
from a_users.models import Profile


class UserResponse(TypedDict):
    username: NotRequired[str | None]
    email: NotRequired[str | None]
    avatar: NotRequired[str | None]


def serialize_user(user: User | None) -> UserResponse:
    if not user:
        return {}
    return {
        "username": user.username,
        "email": user.email,
        "avatar": cast(Profile, getattr(user, "profile")).avatar_url,
    }


def serialize_chat_list(user: User, groups: QuerySet[ChatGroup]):
    return [
        {
            "group_name": group.group_name,
            "member": serialize_user(
                group.members.exclude(id=getattr(user, "id")).first()
            ),
        }
        for group in groups
    ]

from django.contrib.auth.models import User

from a_rtchat.models import ChatGroup


def get_private_chats_for_user(user: User):
    return (
        ChatGroup.objects.filter(members=user)
        .filter(is_private=True)
        .prefetch_related("members")
    )

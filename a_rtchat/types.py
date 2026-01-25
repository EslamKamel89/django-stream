from typing import TypedDict


class AuthorResponse(TypedDict):
    id: int
    username: str
    avatar: str


class MessageResponse(TypedDict):
    id: int
    body: str
    author: AuthorResponse

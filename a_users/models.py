from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static


class ProfileManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related("user")


class Profile(models.Model):
    id: int
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="avatars/", null=True, blank=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    objects = ProfileManager()

    def __str__(self) -> str:
        return f"Profile({self.user.username})"

    @property
    def name(self):
        return self.display_name or self.user.username

    @property
    def avatar_url(self) -> str:
        if self.image:
            return self.image.url
        return static("images/avatar.svg")

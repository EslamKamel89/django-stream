from django.contrib import admin
from django.utils.html import format_html

from a_users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "display_name", "has_avatar", "avatar_preview")
    search_fields = ("user__username", "user__email", "display_name")
    list_filter = ("image",)
    list_select_related = ("user",)
    fieldsets = (
        (
            "User",
            {
                "fields": ("user",),
            },
        ),
        (
            "Profile Info",
            {
                "fields": ("display_name", "info"),
            },
        ),
        (
            "Avatar",
            {
                "fields": ("image",),
            },
        ),
    )

    @admin.display(boolean=True, description="Avatar")
    def has_avatar(self, obj: Profile) -> bool:
        return bool(obj.image)

    @admin.display(description="Avatar preview")
    def avatar_preview(self, obj: Profile):
        return format_html(
            '<a href="{}"><img src="{}" style="width:40px; height:40px; border-radius:50%;" /></a>',
            obj.image.url if obj.image else "#",
            obj.avatar_url,
        )

from django.urls import URLPattern, path

from . import views

urlpatterns: list[URLPattern] = [
    path("", views.ProfileView.as_view(), name="my-profile"),
    path("edit", views.ProfileEditView.as_view(), name="my-profile-edit"),
    path("onboarding", views.ProfileEditView.as_view(), name="profile-onboarding"),
    path("settings", views.ProfileSettingsView.as_view(), name="profile-settings"),
    path(
        "email-change",
        views.EmailChangeView.as_view(),
        name="email-change",
    ),
    path(
        "email-verify",
        views.SendConfirmationEmailView.as_view(),
        name="email-verify",
    ),
    path("delete-account", views.DeleteAccountView.as_view(), name="delete-account"),
]

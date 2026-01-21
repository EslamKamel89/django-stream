from django.urls import URLPattern, path

from . import views

urlpatterns: list[URLPattern] = [path("", views.ChatView.as_view(), name="chat")]

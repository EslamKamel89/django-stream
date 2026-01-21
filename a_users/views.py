from allauth.account.models import EmailAddress
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from a_users.forms import EmailForm, ProfileForm


class ProfileView(View):
    def get(self, request: HttpRequest, username: str | None = None):
        if username:
            profile = get_object_or_404(User, username=username).profile  # type: ignore
        else:
            try:
                profile = request.user.profile  # type: ignore
            except:
                return redirect(reverse("account_login"))
        return render(request, "a_users/profile.html", context={"profile": profile})


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        profile = request.user.profile  # type: ignore
        form = ProfileForm(instance=profile)
        if request.path == reverse("profile-onboarding"):
            onboarding = True
        else:
            onboarding = False
        return render(
            request,
            "a_users/profile-edit.html",
            context={"form": form, "onboarding": onboarding},
        )

    def post(self, request: HttpRequest):
        profile = request.user.profile  # type: ignore
        form = ProfileForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            profile = form.save()
            messages.success(request, "Your profile updated successfully")
            return redirect(reverse("my-profile"))
        messages.error(request, "Please fix the validation error")
        return render(request, "a_users/profile-edit.html", context={"form": form})


class ProfileSettingsView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        return render(request, "a_users/profile-settings.html")


class EmailChangeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        if request.htmx:  # type: ignore
            form = EmailForm(instance=request.user)  # type: ignore
            return render(request, "a_users/partials/email-form.html", {"form": form})
        return redirect(reverse("home"))

    def post(self, request: HttpRequest):
        user: User = request.user  # type: ignore
        if request.POST.get("email") == user.email:
            messages.info(request, "This is already your current email address")
            return redirect(reverse("profile-settings"))
        form = EmailForm(instance=user, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if EmailAddress.objects.filter(email=email).exclude(user=user).exists():  # type: ignore
                messages.warning(request, "Email is already in use")
                return redirect(reverse("profile-settings"))
            form.save()
            email_address = EmailAddress.objects.filter(
                user=user,
                email=email,
                primary=True,
            ).first()
            if email_address:
                email_address.send_confirmation(request)
            messages.success(
                request, "Email updated. Please check your inbox to verify it."
            )
            return redirect(reverse("profile-settings"))
        messages.error(request, "Please fix the validation error")
        return redirect(reverse("profile-settings"))


class SendConfirmationEmailView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        user: User = request.user  # type: ignore
        email_address = EmailAddress.objects.filter(
            user=user, email=user.email, primary=True
        ).first()
        if email_address is None:
            messages.error(
                request,
                "No email address found to verify. Please update your email first.",
            )
        elif email_address.verified:
            messages.info(request, "Your email address is already verified.")
        else:
            email_address.send_confirmation(request)
            messages.success(
                request, "Verification email sent. Please check your inbox."
            )
        return redirect(reverse("profile-settings"))


class DeleteAccountView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        return render(request, "a_users/profile-delete.html")

    def post(self, request: HttpRequest):
        user: User = request.user  # type: ignore
        logout(request)
        user.delete()
        return redirect(reverse("home"))

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse

from a_users.models import Profile

INPUT_STYLES = (
    "block w-full rounded-md border px-3 py-2 "
    "focus:ring-2 focus:ring-primary focus:border-primary"
)

PASSWORD_STYLES = INPUT_STYLES

SUBMIT_STYLES = (
    "w-full bg-primary text-white font-semibold py-2 rounded-md "
    "hover:bg-primary/90 transition"
)


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = "space-y-4 max-w-lg mx-auto"
        self.helper.layout = Layout(
            Field(
                "image",
                css_class="hidden",
                **{"x-on:change": "previewAvatar(event)", "x-ref": "avatarInput"},
            ),
            Field("display_name", css_class=INPUT_STYLES, **{"x-model": "displayName"}),
            Field("info", css_class=INPUT_STYLES, rows=4),
            Submit("submit", "Save Profile", css_class=SUBMIT_STYLES),
        )

    class Meta:
        model = Profile
        fields = ("image", "display_name", "info")


class EmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = "space-y-4 max-w-lg mx-auto"
        self.helper.form_action = reverse("email-change")
        self.helper.layout = Layout(
            Field("email", css_class=INPUT_STYLES, **{"x-model": "displayName"}),
            Div(
                Submit("submit", "Save", css_class=SUBMIT_STYLES),
                HTML(
                    """
                   <a
                    id="email-edit"
                    href="{% url 'profile-settings' %}"
                    class="button !px-2 gray cursor-pointer bg-red-500 flex items-center justify-center"
                    >
                    Cancel
                </a>
                 """
                ),
                css_class="flex w-fit items-center space-x-1",
            ),
        )

    class Meta:
        model = User
        fields = ("email",)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django.forms import ModelForm

from .models import *


class GroupMessageCreateForm(ModelForm):

    class Meta:
        model = GroupMessage
        fields = ("body",)
        labels = {
            "body": "",
        }

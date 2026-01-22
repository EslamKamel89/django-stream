from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django.forms import ModelForm

from .models import *


class GroupMessageCreateForm(ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_method = "POST"
    #     self.helper.form_class = "flex items-center gap-2"
    #     self.helper.layout = Layout(
    #         Div(
    #             Field(
    #                 "body",
    #                 css_class="flex-grow",
    #                 placeholder="Add message…",
    #                 rows=1,
    #                 maxlength="150",
    #             ),
    #             css_class="flex-grow",
    #         ),
    #         HTML(
    #             """
    #     <button type="submit" class="!px-4 !bg-transparent">
    #       <i class="bi bi-send-fill text-primary text-2xl"></i>
    #     </button>
    #              """
    #         ),
    #     )

    class Meta:
        model = GroupMessage
        fields = ("body",)
        labels = {
            "body": "",
        }

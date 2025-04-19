from abc import abstractmethod

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.translation import gettext_lazy as _
import re
from django.core.exceptions import ValidationError


class BaseHelper(FormHelper):
    def __init__(self):
        super().__init__()

        self.add_input(Submit("submit", _("Submit"), css_class="btn-primary"))
        self.form_method = "POST"


class HelperWithoutSubmitAndFormTags(FormHelper):
    def __init__(self):
        self.form_tag = False
        super().__init__()


def validate_international_phone_number(value):
    pattern = r'^\+\d{1,3}\d{6,15}$'
    if not re.match(pattern, value):
        raise ValidationError(
            'The phone number must start with a + sign and an international dialing code, and can only contain numbers (e.g., +36201234567).'
        )


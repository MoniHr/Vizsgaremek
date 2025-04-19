from typing import TypedDict

from django import forms
from django.utils.translation import gettext_lazy as _


class ContactUsData(TypedDict):
    name: str
    email: str
    text: str


class ContactForm(forms.Form):
    name = forms.CharField(label=_("Your name"))
    email = forms.EmailField(label=_("Your email"))
    text = forms.CharField(label=_("Text"))

    cleaned_data: ContactUsData  # typehint

from django import forms
from apps.profile.models import LanguageChoice, Profile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# class LanguageModelForm(forms.ModelForm):
#     class Meta:
#         model = LanguageChoice
#         fields = ['name']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'Save'))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['internal_communication_languages']  # vagy ['__all__'] ha többet is akarsz

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))






class LanguageChoiceForm(forms.Form):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hu', 'Hungarian'),
        ('de', 'German'),
    ]

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

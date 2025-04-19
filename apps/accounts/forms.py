from django import forms
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import SelectableUserType, User, UserType, AvailableLanguageChoices
from apps.core.choices import AvailableLanguageChoices
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.ModelForm):
    name_or_company_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    user_type = forms.ChoiceField(
        label=_("User Type"),
        choices=SelectableUserType.choices,
        initial=SelectableUserType.EMPLOYEE,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    language = forms.ChoiceField(
        label=_("Preferred Language"),
        choices=AvailableLanguageChoices.choices,
        initial=AvailableLanguageChoices.ENGLISH,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("email", "user_type", "language")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user_type = self.data.get("user_type") or self.initial.get("user_type", SelectableUserType.EMPLOYEE)
        self.fields["name_or_company_name"].label = _("Company Name") if user_type == UserType.COMPANY else _("Full Name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("The two password fields didn’t match."))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

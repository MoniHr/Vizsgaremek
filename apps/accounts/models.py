import hashlib
import random
from datetime import datetime
from typing import Union

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.accounts.user_manager import UserManager
from apps.core.choices import AvailableLanguageChoices


class SelectableUserType(models.TextChoices):
    EMPLOYEE = "EMPLOYEE", _("Employee")
    COMPANY = "COMPANY", _("Company")
    FREELANCER = "FREELANCER", _("Freelancer")

class UserType(models.TextChoices):
    ADMINISTRATOR = "ADMINISTRATOR", _("Administrator")
    FREELANCER = "FREELANCER", _("Freelancer")
    COMPANY = "COMPANY", _("Company")
    EMPLOYEE = "EMPLOYEE", _("Employee")

class User(AbstractBaseUser, PermissionsMixin):
    username = None
    USERNAME_FIELD = "email"
    email = models.EmailField(_("email address"), unique=True)
    REQUIRED_FIELDS = []
    objects = UserManager()

    user_type = models.TextField(choices=UserType.choices, null=True)
    rel_company = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    language = models.CharField(
        choices=AvailableLanguageChoices.choices,
        default=AvailableLanguageChoices.ENGLISH,
    )

    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active."
    )

    @cached_property
    def company(self) -> Union["User", None]:
        """
        Returns the company user for this user instance.
        If the current user holds the company account it returns self, otherwise the rel_company field
        If the user is not a Company or CompanyEmployee returns None
        :return:
        """
        match self.user_type:
            case UserType.COMPANY:
                return self
            case UserType.FREELANCER:
                return self
        return None

    @cached_property
    def base_user(self) -> "User":
        if self.user_type in [UserType.COMPANY]:
            return self.company
        return self

    @cached_property
    def active_job_posts(self):
        return self.jobpost_set.filter(is_active=True)

    @property
    def formatted_id(self):
        return f"UD{str(self.id).zfill(6)}"


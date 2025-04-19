from django.db import models
from django.utils.translation import gettext_lazy as _


class SortingChoices(models.TextChoices):
    NEWEST = "NEWEST", _("newest")
    OLDEST = "OLDEST", _("oldest")

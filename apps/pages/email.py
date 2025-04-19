from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.pages.forms import ContactUsData


def send_contact_us_email(data: ContactUsData):
    pass
    # send_email(
    #     _("Contact us"),
    #     settings.DEFAULT_FROM_EMAIL,
    #     [settings.DEFAULT_FROM_EMAIL],
    #     "pages/email/contact-us.html",
    #     data,
    # )

from django.urls import path
from apps.pages.views import index, template_response, contact

urlpatterns = [
    path("", index, name="index"),
    path("about/", template_response, {"template": "pages/about.html"}, name="about"),
    path("contact/", template_response, {"template": "pages/contact.html"}, name="contact"),
    path("faqs/", template_response, {"template": "pages/faqs.html"}, name="faqs"),
    path("pricing/", template_response, {"template": "pages/pricing.html"}, name="pricing"),
    path("services/", template_response, {"template": "pages/services.html"}, name="services"),
    path("terms-and-conditions/", template_response, {"template": "pages/terms-and-conditions.html"}, name="terms-and-conditions"),
    path("contact-us/", contact, name="contact_us"),
]

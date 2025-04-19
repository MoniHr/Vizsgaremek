from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import UserType
from apps.core.tasks import send_email_task
from .forms import SignupForm
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.user_type = form.cleaned_data["user_type"]
                    user.language = form.cleaned_data["language"]
                    user.save()

                    profile = user.profile
                    if user.user_type == UserType.COMPANY:
                        profile.company_name = form.cleaned_data["name_or_company_name"]
                    else:
                        profile.public_name = form.cleaned_data["name_or_company_name"]
                    profile.save()

                    # 📧 Email küldés
                    name = profile.company_name if user.user_type == UserType.COMPANY else profile.public_name

                    send_email_task.delay(
                        subject="Welcome to Our Platform!",
                        recipient_email=[str(user.email)],
                        context={"name": name},
                        template_name="emails/welcome.html"
                    )

                login(request, user)
                messages.success(request, _("Registration successful!"))
                return redirect("edit_profile")

            except Exception as e:
                messages.error(request, str(e))

    else:
        form = SignupForm()

    return render(request, "accounts/register.html", {"form": form})



from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.db.models import Count, Q
from apps.pages.forms import ContactForm, ContactUsData, ProfileForm, LanguageChoiceForm
from apps.job_post.models import Category


def index(request):
    model_form = ProfileForm()
    choice_form = LanguageChoiceForm()

    categories = Category.objects.annotate(
        active_job_count=Count('category_job_posts', filter=Q(category_job_posts__is_active=True))
    ).filter(featured=True).values('name', 'id', 'active_job_count', 'icon').order_by('order')[:12]

    context = {
        "categories": list(categories),
        'model_form': model_form,
        'choice_form': choice_form,
    }
    return render(request, "pages/index.html", context)


def template_response(request, template):
    if not template:
        raise ValueError("Template not provided in path definition!")
    return render(request, template)


@login_required
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest()

        data: ContactUsData = form.cleaned_data
        # send_contact_us_email(data)

        return redirect("/")

    return HttpResponseBadRequest()

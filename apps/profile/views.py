import io
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from apps.accounts.models import User, UserType
from apps.core.forms import HelperWithoutSubmitAndFormTags
from apps.core.tasks import send_email_task
from apps.job_post.models import JobPost, JobPostApplication
from apps.profile.forms import CVEditForm, CVForm, CompanyProfileForm, CompanySelectionForm, CoverLetterForm, CreateLanguageKnowledgeForm, DocumentEditForm, DocumentForm, EducationForm, EmailForm, EmployeeProfileForm, WorkExperienceForm
from apps.profile.models import CV, CoverLetter, Document, Education, LanguageKnowledge, Profile, SubActivity, WorkExperience
from apps.profile.pdf_generator import PdfGenerator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import  BadHeaderError
import logging
from django.core.mail import BadHeaderError

logger = logging.getLogger(__name__)



@login_required
def edit_profile_view(request):
    user = request.user
    user_type = user.user_type


    # 🌟 Egyéb felhasználók (COMPANY, FREELANCER, EMPLOYEE)
    missing_fields = user.profile.get_missing_required_fields()

    if user_type == UserType.COMPANY:
        form_class = CompanyProfileForm
    elif user_type == UserType.EMPLOYEE:
        form_class = EmployeeProfileForm
    elif user_type == UserType.FREELANCER:
        form_class = CompanyProfileForm if request.GET.get("p") == "1" else EmployeeProfileForm
    else:
        raise NotImplementedError(f"Unknown user type: {user_type}")

    instance = user.profile

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            with transaction.atomic():
                profile = form.save(commit=False)
                profile.user = user

                profile.save()
                form.save_m2m()

                messages.success(request, "Profile successfully updated!")
            return redirect(reverse("edit_profile"))
    else:
        form = form_class(instance=instance)

    context = {
        "form": form,
        "helper": HelperWithoutSubmitAndFormTags(),
        "missing_fields": missing_fields,
    }
    return render(request, "dashboard/common/edit_profile.html", context)


@login_required
def list_work_experience(request):
    profile = request.user.profile
    work_experience_list = WorkExperience.objects.filter(profile=profile)

    context = {
        "work_experience_list": work_experience_list,
    }

    return render(request, "dashboard/common/list_work_experience.html", context)

@login_required
def create_work_experience(request):
    profile = request.user.profile
    form = WorkExperienceForm()

    if request.method == "POST":
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.profile = profile
            form.save()
            return redirect("list_work_experience")

    return render(request, "dashboard/common/create_work_experience.html", {"form": form})

@login_required
def delete_work_experience(request, pk):
    work_experience = get_object_or_404(WorkExperience, pk=pk, profile=request.user.profile)
    work_experience.delete()
    return redirect("list_work_experience")

@login_required
def list_education(request):
    profile = request.user.profile
    education_list = Education.objects.filter(profile=profile)

    context = {
        "education_list": education_list,
    }
    return render(request, "dashboard/common/list_education.html", context)

@login_required
def create_education(request):
    profile = request.user.profile
    form = EducationForm()

    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.profile = profile
            education.save()
            return redirect(reverse("list_education"))

    context = {
        "form": form,
        "helper": HelperWithoutSubmitAndFormTags(),
    }
    return render(request, "dashboard/common/create_education.html", context)

@login_required
def delete_education(request, pk):
    education = get_object_or_404(Education, pk=pk, profile=request.user.profile)
    education.delete()
    return redirect(reverse("list_education"))

@login_required
def list_language_knowledge(request):
    profile = request.user.profile
    language_knowledge_list = LanguageKnowledge.objects.filter(profile=profile)

    context = {
        "language_knowledge_list": language_knowledge_list,
    }
    return render(request, "dashboard/common/list_language_knowledge.html", context)

@login_required
def create_language_knowledge(request):
    profile = request.user.profile
    form = CreateLanguageKnowledgeForm()

    if request.method == "POST":
        form = CreateLanguageKnowledgeForm(request.POST)
        if form.is_valid():
            language_knowledge = LanguageKnowledge(
                profile=profile,
                language=form.cleaned_data["language"],
                level=form.cleaned_data["level"],
            )
            language_knowledge.save()
            return redirect(reverse("list_language_knowledge"))

    context = {
        "form": form,
    }
    return render(request, "dashboard/common/create_language_knowledge.html", context)

@login_required
def delete_language_knowledge(request, pk):
    language_knowledge = get_object_or_404(LanguageKnowledge, pk=pk, profile=request.user.profile)
    language_knowledge.delete()
    return redirect(reverse("list_language_knowledge"))

@login_required
# @edit_profile_permission
def language_knowledge_view(request):
    profile = request.user.profile
    language_knowledge_form = CreateLanguageKnowledgeForm()

    if request.method == "POST":
        if "submit_language_knowledge" in request.POST:
            language_knowledge_form = CreateLanguageKnowledgeForm(request.POST)
            if language_knowledge_form.is_valid():
                language_knowledge = language_knowledge_form.save(commit=False)
                language_knowledge.profile = profile
                language_knowledge.save()
                return redirect(reverse("language_knowledge"))

    context = {
        "language_knowledge_form": language_knowledge_form,
        "language_knowledge_list": LanguageKnowledge.objects.filter(profile=profile),
        "helper": HelperWithoutSubmitAndFormTags(),
    }

    return render(request, "dashboard/common/language_knowledge.html", context)

class UserProfileDeleteMixin(View):
	success_url = None

	def post(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.profile != request.user.profile:
			return HttpResponseForbidden()
		obj.delete()
		return redirect(self.success_url)

@login_required
def list_documents(request):
    document_form = DocumentForm()

    if request.method == "POST":
        document_form = DocumentForm(request.POST, request.FILES)
        if document_form.is_valid():
            document = document_form.save(commit=False)
            document.profile = request.user.profile
            document.save()
            return redirect('list_document')

    context = {
        'document_form': document_form,
        'documents': request.user.profile.documents.all(),
    }
    return render(request, 'dashboard/common/list_document.html', context)

@login_required
def list_cv(request):
    cv_form = CVForm()

    if request.method == "POST":
        cv_form = CVForm(request.POST, request.FILES)
        if cv_form.is_valid():
            cv = cv_form.save(commit=False)
            cv.profile = request.user.profile
            cv.save()
            return redirect('list_cv')

    context = {
        'cv_form': cv_form,
        'cvs': request.user.profile.cvs.all(),
    }
    return render(request, 'dashboard/common/list_cv.html', context)

@login_required
def list_cover_letters(request):
    cover_letter_form = CoverLetterForm()

    if request.method == "POST":
        cover_letter_form = CoverLetterForm(request.POST, request.FILES)
        if cover_letter_form.is_valid():
            cover_letter = cover_letter_form.save(commit=False)
            cover_letter.profile = request.user.profile
            cover_letter.save()
            return redirect('list_cover_letter')

    context = {
        'cover_letter_form': cover_letter_form,
        'cover_letters': request.user.profile.cover_letters.all(),
    }
    return render(request, 'dashboard/common/list_cover_letter.html', context)

@login_required
def create_cover_letter(request):
    if request.method == "POST":
        form = CoverLetterForm(request.POST, request.FILES)
        if form.is_valid():
            cover_letter = form.save(commit=False)
            cover_letter.profile = request.user.profile
            cover_letter.save()
            return redirect('list_cover_letter')

    else:
        form = CoverLetterForm()

    return render(request, "dashboard/common/create_cover_letter.html", {"form": form})

@login_required
def create_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.profile = request.user.profile
            document.save()
            return redirect('list_document')

    else:
        form = DocumentForm()

    return render(request, "dashboard/common/create_document.html", {"form": form})

@login_required
def edit_document(request, pk):
    document = get_object_or_404(Document, pk=pk, profile=request.user.profile)

    if request.method == "POST":
        form = DocumentEditForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect(reverse("list_document"))
    else:
        form = DocumentEditForm(instance=document)

    return render(request, "dashboard/common/edit_document.html", {"form": form})

@login_required
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk, profile=request.user.profile)

    if document.profile != request.user.profile:
        return HttpResponseForbidden()

    document.delete()
    return redirect(reverse("list_document"))

@login_required
def create_cv(request):
    if request.method == "POST":
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.profile = request.user.profile
            cv.save()
            return redirect('list_cv')

    else:
        form = CVForm()

    return render(request, "dashboard/common/create_cv.html", {"form": form})

@login_required
def edit_cv(request, pk):
    cv = get_object_or_404(CV, pk=pk, profile=request.user.profile)

    if request.method == "POST":
        form = CVEditForm(request.POST, request.FILES, instance=cv)
        if form.is_valid():
            form.save()
            return redirect(reverse("list_cv"))
    else:
        form = CVEditForm(instance=cv)

    return render(request, "dashboard/common/edit_cv.html", {"form": form})

@login_required
def delete_cv(request, pk):
    cv = get_object_or_404(CV, pk=pk, profile=request.user.profile)

    if cv.profile != request.user.profile:
        return HttpResponseForbidden()

    cv.delete()
    return redirect(reverse("list_cv"))

@login_required
def edit_cover_letter(request, pk):
    cover_letter = get_object_or_404(CoverLetter, pk=pk, profile=request.user.profile)

    if request.method == "POST":
        form = CoverLetterForm(request.POST, request.FILES, instance=cover_letter)
        if form.is_valid():
            form.save()
            return redirect(reverse("list_cover_letter"))
    else:
        form = CoverLetterForm(instance=cover_letter)

    return render(request, "dashboard/common/edit_cover_letter.html", {"form": form})

@login_required
def delete_cover_letter(request, pk):
    cover_letter = get_object_or_404(CoverLetter, pk=pk, profile=request.user.profile)

    if cover_letter.profile != request.user.profile:
        return HttpResponseForbidden()

    cover_letter.delete()
    return redirect(reverse("list_cover_letter"))

@login_required
def public_profile(request, slug):
    profile = get_object_or_404(Profile.objects.select_related("user", "activity", "sub_activity"), slug=slug)
    user_type = profile.user.user_type

    # Ha van átadott application_id, akkor állítsuk be is_read=True
    application_id = request.GET.get("application_id")
    if application_id and request.user.is_authenticated:
        try:
            application = JobPostApplication.objects.get(id=application_id, user=profile.user, job__created_by=request.user)
            if not application.is_read:
                application.is_read = True
                application.save()
        except JobPostApplication.DoesNotExist:
            pass  # Biztonsági okból ne dobjunk hibát, ha nem található

    # Template kiválasztás
    if user_type == UserType.COMPANY:
        template_name = "profile/company/detail.html"
    elif user_type == UserType.FREELANCER:
        template_name = "profile/freelancer/detail.html"
    else:
        template_name = "profile/employee/detail.html"

    active_jobs = None
    if user_type in [UserType.COMPANY, UserType.FREELANCER]:
        active_jobs = JobPost.objects.filter(
            created_by=profile.user, is_active=True
        ).select_related("category", "sub_category", "job_location").order_by("-created_at")

    documents = Document.objects.filter(profile=profile, is_public=True)
    cvs = CV.objects.filter(profile=profile, is_public=True)
    cover_letters = CoverLetter.objects.filter(profile=profile, is_public=True)

    context = {
        "profile": profile,
        "documents": documents,
        "cvs": cvs,
        "cover_letters": cover_letters,
        "email_form": EmailForm(),
        "active_jobs": active_jobs,
    }

    return render(request, template_name, context)

@login_required
def blocked_company_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    blocked_companies = profile.blocked_companies.all()

    return render(
        request,
        "dashboard/common/list_blocked_company.html",
        {"profile": profile, "blocked_companies": blocked_companies},
    )

@login_required
def edit_blocked_company(request):
    if request.method == "POST":
        form = CompanySelectionForm(request.POST, user=request.user)
        if form.is_valid():
            profile = get_object_or_404(Profile, user=request.user)
            company = form.cleaned_data["company"]
            profile.blocked_companies.add(company)
            return redirect(reverse("list_blocked_company"))
    else:
        form = CompanySelectionForm(user=request.user)

    return render(
        request, "dashboard/common/edit_blocked_company.html", {"form": form}
    )

@login_required
def delete_blocked_company(request, pk):
    if request.method == "POST":
        profile = get_object_or_404(Profile, user=request.user)
        company_to_remove = get_object_or_404(User, pk=pk)
        profile.blocked_companies.remove(company_to_remove)
        return redirect("list_blocked_company")

    return HttpResponse(status=405)


@login_required
def change_profile_image(request):
    if request.method == "POST" and request.FILES.get("profile_picture"):
        profile = request.user.profile

        if request.user.user_type in ["COMPANY", "COMPANY_EMPLOYEE"]:
            profile.company_logo = request.FILES["profile_picture"]
        else:
            profile.profile_picture = request.FILES["profile_picture"]

        profile.save()
        return redirect("edit_profile")

    return HttpResponse(status=405)  # Method Not Allowed

@login_required
def generate_cv(request):
    cv_html = render_to_string("profile/employee/cv-template.html", {"user": request.user})
    generator = PdfGenerator()
    pdf = generator.generate(cv_html)
    file = io.BytesIO(pdf)

    return HttpResponse(file, content_type="application/pdf")

def load_sub_activities(request):
    activity_id = request.GET.get("activity")
    sub_activities = SubActivity.objects.filter(activity_id=activity_id).order_by("name")

    return JsonResponse({"html": render_to_string("profile/company/sub_activities_options.html", {"sub_activities": sub_activities})})



def send_email_view(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            profile_slug = request.POST.get("slug")
            profile = get_object_or_404(Profile, slug=profile_slug)
            user = profile.user
            recipient_email = profile.company_email or user.email

            # Űrlap mezők
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            # 🔀 Sablon kiválasztása felhasználó típusa alapján
            match user.user_type:
                case UserType.FREELANCER:
                    template = "emails/contact_freelancer.html"
                case UserType.EMPLOYEE:
                    template = "emails/contact_employer.html"
                case UserType.COMPANY:
                    template = "emails/contact_company.html"
                case _:
                    template = "emails/contact_general.html"

            context = {
                "profile_name": profile.public_name or profile.company_name or user.email,
                "sender_name": name,
                "sender_email": email,
                "message": message,
            }

            try:
                # 🚀 Email Celery-n keresztül
                send_email_task.delay(
                    subject=subject,
                    recipient_email=recipient_email,
                    context=context,
                    template_name=template
                )
                messages.success(request, "Email is being sent!")
                logger.info(f"🚀 Async email task sent to {recipient_email}")
                return redirect(request.META.get("HTTP_REFERER", "/"))

            except BadHeaderError:
                messages.error(request, "Invalid email header.")
                logger.exception("❌ Invalid email header.")
            except Exception as e:
                messages.error(request, f"Email sending failed: {str(e)}")
                logger.exception(f"❌ Failed to trigger email task: {e}")
        else:
            messages.error(request, "Form validation failed.")
            logger.warning("⚠ Form érvénytelen!")
    else:
        messages.error(request, "Invalid request method.")

    return redirect(request.META.get("HTTP_REFERER", "/"))

def send_simple_email(request):
    send_email_task.delay(
        subject="Welcome!",
        recipient_email="sikler.sikler@gmail.com",
        context={"name": "Angela"},
        template_name="emails/welcome.html"
    )
    return HttpResponse("✅ Email elküldve sikeresen!")

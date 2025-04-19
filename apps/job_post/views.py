from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count, Q
from django.urls import reverse
from apps.job_post.forms import ApplyJobForm, EmailJobForm, JobPostForm
from apps.job_post.models import JobPlan, JobPost, JobPostApplication, SubCategory, Category
from apps.pages.forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
import shutil
import os
from django.views.decorators.http import require_POST
import stripe
from django.conf import settings
import logging
from django.utils.timezone import now
from django.core.mail import send_mail, BadHeaderError
logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY



def load_sub_categories(request):
    category_id = request.GET.get('category')
    sub_categories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse(render_to_string('job_post/jobs/sub_category_options.html', {'sub_categories': sub_categories}), safe=False)

def index(request):
    categories = Category.objects.annotate(
        active_job_count=Count('category_job_posts', filter=Q(category_job_posts__is_active=True))
    ).filter(featured=True).values('name', 'id', 'active_job_count', 'icon').order_by('order')[:12]

    return render(request, "pages/index.html", {'categories': list(categories)})

def template_response(request, template):
    if not template:
        raise ValueError("Template not provided in path definition!")
    return render(request, template)

@login_required
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # send_contact_us_email(data)
            return redirect("/")
        return HttpResponseBadRequest()
    return render(request, "pages/contact.html", {"form": ContactForm()})


@login_required
def job_apply(request, slug):
    job = get_object_or_404(JobPost, slug=slug)

    if JobPostApplication.objects.filter(job=job, user=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect("job_detail", slug=job.slug)

    if request.method == "POST":
        form = ApplyJobForm(request, job, request.POST)
        if form.is_valid():
            with transaction.atomic():
                application = JobPostApplication(
                    user=request.user,
                    job=job,
                    text=form.cleaned_data.get("text", "")
                )

                if form.cleaned_data.get("cv_id"):
                    original_cv = form.cleaned_data["cv_id"]
                    application.cv = clone_file(original_cv.cv_file, "cv")

                if form.cleaned_data.get("cover_letter_id"):
                    original_cover_letter = form.cleaned_data["cover_letter_id"]
                    application.cover_letter = clone_file(original_cover_letter.cover_letter_file, "cover_letter")

                application.save()

            messages.success(request, "Your application has been submitted successfully!")
            return redirect(job.get_absolute_url())
    else:
        form = ApplyJobForm(request, job)

    return render(request, "job_post/jobs/job_apply.html", {"form": form, "job": job})

def clone_file(original_file, file_type):
    if not original_file:
        return None

    original_path = original_file.path
    file_extension = os.path.splitext(original_path)[1]  # Pl.: .pdf, .docx

    upload_dir = os.path.join(settings.MEDIA_ROOT, "job_applications")

    os.makedirs(upload_dir, exist_ok=True)

    new_filename = f"{file_type}_copy_{os.path.basename(original_path)}"
    new_path = os.path.join(upload_dir, new_filename)

    shutil.copyfile(original_path, new_path)

    return f"job_applications/{new_filename}"


@login_required
def job_my_applications(request):
    applications = JobPostApplication.objects.filter(user=request.user)
    return render(request, "job_post/jobs/job_my_applications.html", {"applications": applications})

@login_required
def job_applications(request):
    applications = JobPostApplication.objects.filter(job__created_by=request.user).select_related('job', 'user', 'user__profile')
    return render(request, "job_post/jobs/job_applications.html", {"applications": applications})


@login_required
def delete_application(request, application_id):
    application = get_object_or_404(JobPostApplication, id=application_id)

    if application.user != request.user:
        messages.error(request, "You don't have permission to delete this application.")
        return redirect("my_applications")

    application.delete()
    messages.success(request, "Application deleted successfully.")
    return redirect("my_applications")

@login_required
def wishlist_toggle(request, job_slug):
    job = get_object_or_404(JobPost, slug=job_slug)
    was_added = request.user.saved_jobs.filter(slug=job_slug).exists()

    if was_added:
        request.user.saved_jobs.remove(job)
    else:
        request.user.saved_jobs.add(job)

    return JsonResponse({"status": "success", "added": not was_added})

@login_required
def wishlist_view(request):
    wishlist_jobs = request.user.saved_jobs.filter(is_active=True)
    return render(request, "job_post/jobs/wishlist.html", {"wishlist_jobs": wishlist_jobs})

@login_required
def list_jobs_view(request):
    jobs = JobPost.objects.filter(created_by=request.user.company)
    return render(request, "job_post/jobs/list_jobs.html", {"jobs": jobs, "now": now()})

@login_required
def create_job_post(request):
    if request.method == "POST":
        form = JobPostForm(request.POST, user=request.user)

        if form.is_valid():
            with transaction.atomic():
                job_post = form.save(commit=False)
                job_post.is_active = True

                if hasattr(request.user, "company"):
                    job_post.created_by = request.user.company
                else:
                    messages.error(request, "You must be a company to post a job.")
                    return redirect("create_job")

                job_post.save()

                form.save_m2m()

            messages.success(request, "Job post created successfully!")
            return redirect("list_jobs")
        else:
            messages.error(request, "There was an error in your form submission.")

    else:
        form = JobPostForm(user=request.user)

    return render(request, "job_post/jobs/create.html", {"form": form})


@login_required
def edit_job_post(request, slug):
    job_post = get_object_or_404(JobPost, slug=slug, created_by=request.user.company)

    if request.method == "POST":
        form = JobPostForm(request.POST, instance=job_post, user=request.user)
        if form.is_valid():
            try:
                with transaction.atomic():
                    job_post = form.save(commit=False)
                    job_post.created_by = request.user.company
                    job_post.save()

                    form.save_m2m()

                messages.success(request, "Job post updated successfully!")
                return redirect("list_jobs")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobPostForm(instance=job_post, user=request.user)

    return render(request, "job_post/jobs/edit.html", {"form": form, "job_post": job_post})

@login_required
def delete_job_post(request, job_slug):
    job = get_object_or_404(JobPost, slug=job_slug)
    job.delete()
    return redirect("list_jobs")


def send_email_job(request):
    if request.method == "POST":
        form = EmailJobForm(request.POST)

        if form.is_valid():
            job_id = request.POST.get("id")
            job = get_object_or_404(JobPost, id=job_id)

            recipient_email = (
                job.created_by.profile.company_email
                if hasattr(job.created_by, "profile") and job.created_by.profile.company_email
                else job.created_by.email
            )

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            full_message = f"Name: {name}\nEmail: {email}\n\n{message}"

            try:

                send_mail(
                    subject,
                    full_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient_email],
                    fail_silently=False
                )

                messages.success(request, "✅ Email successfully sent!")
                logger.info("✅ Email sikeresen elküldve!")
                return redirect(request.META.get("HTTP_REFERER", "/"))

            except BadHeaderError:
                logger.error("❌ Hiba: Érvénytelen e-mail fejléc.")
                messages.error(request, "Invalid email header.")

            except Exception as e:
                logger.exception(f"❌ Email küldési hiba: {str(e)}")
                messages.error(request, f"Email sending failed: {str(e)}")

        else:
            logger.warning("⚠ Form érvénytelen!")
            logger.debug(f"❌ Form hibák: {form.errors}")

    else:
        logger.warning("⚠ Nem POST kérés érkezett!")

    messages.error(request, "❌ Invalid request.")
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def boost_job_post(request, slug):
    job = get_object_or_404(JobPost, slug=slug)
    profile = request.user.profile

    available_plans = JobPlan.objects.filter(is_active=True).order_by("price")

    context = {
        "job": job,
        "plans": available_plans,
        "profile": profile,
    }

    return render(request, "job_post/jobs/boost_plan_selection.html", context)



@require_POST
def stripe_checkout_start(request, slug):
    plan_id = request.POST.get("plan_id")
    if not plan_id:
        return HttpResponseBadRequest("Missing plan ID.")

    job = get_object_or_404(JobPost, slug=slug)
    plan = get_object_or_404(JobPlan, pk=plan_id)

    # Stripe metadata - optional (used in webhook if needed)
    metadata = {
        "job_post_id": str(job.id),
        "plan_id": str(plan.id),
        "user_id": str(request.user.id),
    }

    # Create Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        customer_email=request.user.email,
        billing_address_collection="required",
        metadata=metadata,
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": plan.name,
                    "description": plan.description or "Boost Plan",
                },
                "unit_amount": int(plan.price * 100),
            },
            "quantity": 1,
        }],
        success_url=request.build_absolute_uri(
            reverse("boost_success", kwargs={"slug": slug})
        ),
        cancel_url=request.build_absolute_uri(
            reverse("boost_choose_plan", kwargs={"slug": slug})
        ),
    )

    return redirect(checkout_session.url)


def stripe_success(request, slug):
    return render(request, "job_post/jobs/stripe_success.html", {"job_slug": slug})

def stripe_cancel(request):
    return render(request, "job_post/jobs/stripe_cancel.html")

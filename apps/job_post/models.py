from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.choices import LanguageChoices, LanguageKnowledgeLevelChoices
from apps.profile.models import DrivingLicenseChoice, EducationChoice, EmploymentScheduleChoice, LocationChoice, WorkingTimeChoice
from slugify import slugify
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone


User = get_user_model()


BOOST_LOCATION_CHOICES = [
    ("homepage", "Főoldal"),
    ("banner", "Banner"),
    ("sidebar", "Oldalsáv"),
]

class RequiredLanguageKnowledge(models.Model):
    language = models.CharField(choices=LanguageChoices.choices, max_length=100, blank=True, null=True)
    level = models.TextField(choices=LanguageKnowledgeLevelChoices.choices, blank=True, null=True)
    job_post = models.ForeignKey("JobPost", on_delete=models.CASCADE, related_name="required_languages", null=True, blank=True)

    def __str__(self):
        return f"{self.language}" if self.language else "No language requirement"


class Category(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True, null=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('category', 'code')
        verbose_name = _("Sub Category")
        verbose_name_plural = _("Sub Categories")


BOOST_LOCATION_CHOICES = [
    ("homepage", "Főoldal"),
    ("banner", "Banner"),
    ("sidebar", "Oldalsáv"),
]

class JobPlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ("standard", "Standard Listing"),
        ("homepage", "Homepage Boost"),
        ("banner", "Banner Boost"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_days = models.PositiveIntegerField(default=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    plan_type = models.CharField(max_length=50, choices=PLAN_TYPE_CHOICES)
    is_recommended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.duration_days} days) – ${self.price}"


class JobPost(models.Model):
    # --- Alap mezők ---
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="category_job_posts")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True, related_name="sub_category_job_posts")

    job_description = models.TextField()
    expectations = models.TextField()
    educations = models.ManyToManyField(EducationChoice, blank=True)
    driving_license = models.ManyToManyField(DrivingLicenseChoice, blank=True)
    advantages = models.TextField()
    working_time = models.ManyToManyField(WorkingTimeChoice, blank=True)
    work_schedule = models.ManyToManyField(EmploymentScheduleChoice, blank=True)

    job_location = models.ForeignKey(LocationChoice, on_delete=models.CASCADE, null=True, blank=True, related_name="job_location_job_posts")
    job_city = models.CharField(max_length=254)
    job_address = models.CharField(max_length=254)
    benefits = models.TextField()

    is_cv_required = models.BooleanField(default=False)
    is_cover_letter_required = models.BooleanField(default=False)

    contact_email = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255)

    saved_by = models.ManyToManyField(User, related_name="saved_jobs", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_posts")

    # --- BOOST rendszer ---
    is_boosted = models.BooleanField(default=False)
    boost_start_date = models.DateTimeField(null=True, blank=True)
    boost_end_date = models.DateTimeField(null=True, blank=True)
    boost_location = models.CharField(max_length=50, choices=BOOST_LOCATION_CHOICES, null=True, blank=True)
    selected_plan = models.ForeignKey(JobPlan, on_delete=models.SET_NULL, null=True, blank=True)


    # Stripe transaction tracking
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_checkout_session_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_customer_email = models.EmailField(null=True, blank=True)
    stripe_transaction_completed_at = models.DateTimeField(null=True, blank=True)


    # Billing Information (for invoicing & Stripe metadata)
    billing_name = models.CharField(max_length=255, null=True)
    billing_tax_number = models.CharField(max_length=100, null=True)
    billing_address = models.CharField(max_length=255, null=True)
    billing_state = models.CharField(max_length=100, null=True)
    billing_country = models.CharField(max_length=100, null=True)
    billing_city = models.CharField(max_length=100, null=True)
    billing_zip_code = models.CharField(max_length=20, null=True)


    # --- Cím szerkeszthetősége ---
    title_editable_until = models.DateTimeField(null=True, blank=True)

    # --- Emlékeztető logikához ---
    expiration_reminder_sent = models.BooleanField(default=False)
    reminder_days_before_expiry = models.PositiveIntegerField(default=3)  # X nappal előtte

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Slug csak egyszer generálódik
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(self.pk)
            super().save()

        # Ha boost aktiválva van és nincs dátum megadva
        if self.is_boosted and not self.boost_start_date:
            self.boost_start_date = timezone.now()
            self.boost_end_date = self.boost_start_date + timedelta(days=30)  # alapértelmezett 30 nap
            self.title_editable_until = self.boost_start_date + timedelta(days=5)
            super().save()

    def is_boost_expired(self):
        return self.boost_end_date and timezone.now() > self.boost_end_date

    def can_edit_title(self):
        return self.title_editable_until and timezone.now() <= self.title_editable_until

    def should_send_expiration_reminder(self):
        if self.boost_end_date and not self.expiration_reminder_sent:
            days_left = (self.boost_end_date - timezone.now()).days
            return days_left <= self.reminder_days_before_expiry
        return False

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"slug": self.slug})

    def get_map_location(self):
        parts = [self.job_location.name if self.job_location else None, self.job_city, self.job_address]
        return ", ".join(filter(None, parts))

    def __str__(self):
        return self.title


def upload_to_job_post_folder(instance: "JobPostApplication", filename):
    return f"uploads/job_applications/{instance.job.slug}/{instance.user.display_name}/{filename}"

class JobPostApplication(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="applicants")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applied_jobs")
    text = models.TextField(null=True)
    cv = models.FileField(null=True, blank=True, upload_to=upload_to_job_post_folder)
    cover_letter = models.FileField(null=True, blank=True, upload_to=upload_to_job_post_folder)
    is_read = models.BooleanField(default=False)

    def unread_applicants_count(self):
        return self.applicants.filter(is_read=False).count()

    class Meta:
        ordering = ['is_read', '-created_at']

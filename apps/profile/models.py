import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import UserType
from apps.core.choices import LanguageChoices, LanguageKnowledgeLevelChoices
from slugify import slugify
from django.utils import timezone
from django.utils.functional import cached_property
User = get_user_model()


def upload_to_profile_folder(instance, filename):
    return f"uploads/user/{instance.user.pk}/profile/{filename}"

def upload_to_profile_cv_folder(instance, filename):
    return f"uploads/user/{instance.profile.user.pk}/profile/cv/{filename}"

def upload_to_profile_cover_letter_folder(instance, filename):
    return f"uploads/user/{instance.profile.user.pk}/profile/cover_letter/{filename}"

def upload_to_profile_document_folder(instance, filename):
    return f"uploads/user/{instance.profile.user.pk}/profile/document/{filename}"

class Activity(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

class SubActivity(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="activities")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('activity', 'code')
        verbose_name = _("Subactivity")
        verbose_name_plural = _("Subactivities")

class LocationChoice(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Job Location Choice")
        verbose_name_plural = _("Job Location Choices")

class NumberOfWorkerChoice(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Number Of Worker Choice")
        verbose_name_plural = _("Number Of Workers Choices")

class EducationChoice(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    custom_order = models.IntegerField(null=True, blank=True)  # Hozzáadott mező

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Education Choice")
        verbose_name_plural = _("Education Choices")
        ordering = ['custom_order']

class LanguageChoice(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Language Choice")
        verbose_name_plural = _("Language Choices")

class EmploymentScheduleChoice(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Employment Schedule Choice")
        verbose_name_plural = _("Employment Schedule Choices")

class DrivingLicenseChoice(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Driving License Choice")
        verbose_name_plural = _("Driving License Choices")

class WorkingTimeChoice(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Working Time Choice")
        verbose_name_plural = _("Working Time Choices")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(default=uuid.uuid4)

    # Company
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_information = models.TextField(null=True, blank=True)
    company_logo = models.ImageField(null=True, upload_to=upload_to_profile_folder, blank=True)
    phone_number = models.CharField(max_length=14, null=True, blank=True)
    company_email = models.EmailField(max_length=254, null=True, blank=True)

    headquarters = models.CharField(max_length=255, null=True, blank=True)
    year_of_foundation = models.IntegerField(null=True, blank=True)

    number_of_worker = models.ForeignKey(NumberOfWorkerChoice, on_delete=models.SET_NULL, null=True, blank=True)

    internal_communication_languages = models.ManyToManyField(LanguageChoice, blank=True)

    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True, related_name="activity_profile")
    sub_activity = models.ForeignKey(SubActivity, on_delete=models.SET_NULL, null=True, blank=True, related_name="sub_activity_profile")

    website = models.URLField(null=True, blank=True)


    # /Company

    # Common data (freelancer and employee)
    public_name = models.CharField(max_length=255, null=True, blank=True)
    profession = models.CharField(max_length=255, null=True)
    experience = models.CharField(max_length=254, null=True, blank=True)
    qualification = models.CharField(max_length=254, null=True, blank=True)
    achievement = models.CharField(max_length=254, null=True, blank=True)
    introduction = models.TextField(null=True, blank=True, max_length=1000)

    job_location = models.ManyToManyField(LocationChoice, blank=True) #ez alapján lesz a kresés majd még

    # /Common data

    # Employee
    profile_picture = models.ImageField(null=True, blank=True, upload_to=upload_to_profile_folder)
    date_of_birth = models.DateField(null=True, blank=True)

    is_date_of_birth_private = models.BooleanField(null=True, default=False)
    blocked_companies = models.ManyToManyField(User, blank=True, related_name="blocking_users")
    is_contact_private = models.BooleanField(null=True, default=False,help_text=_("If checked only your username show up in chats"),)
    is_address_private = models.BooleanField(null=True, default=False, help_text=_("If checked your address won't show up on your profile page"),)
    is_contact_phone_private = models.BooleanField(null=True, default=False)

    profile_location = models.ForeignKey(LocationChoice, on_delete=models.CASCADE, null=True, blank=True, related_name="profile_location")
    profile_city = models.CharField(max_length=254)
    profile_address = models.CharField(max_length=254)

    work_schedule = models.ManyToManyField(EmploymentScheduleChoice, blank=True)
    driving_license = models.ManyToManyField(DrivingLicenseChoice, blank=True)
    working_time = models.ManyToManyField(WorkingTimeChoice, blank=True)

    is_active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    # /Employee
    def save(self, *args, **kwargs):
        required_fields = []

        if self.user.user_type == 'COMPANY':
            required_fields = [
                self.phone_number,
                self.company_name,
            ]
        elif self.user.user_type in ['EMPLOYEE', 'FREELANCER']:
            required_fields = [
                self.public_name,
                self.profession,
                self.phone_number,
            ]

        # is_active csak akkor True, ha minden required mező ki van töltve
        self.is_active = all(bool(field and str(field).strip()) for field in required_fields)

        # slug generálás, ha nincs
        if not self.slug:
            self.slug = slugify(str(uuid.uuid4()))

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("public_profile", kwargs={"slug": self.slug})

    def get_profile_image_url(self):
        if self.user.user_type == 'COMPANY' and self.company_logo:
            return self.company_logo.url
        elif self.user.user_type in ['FREELANCER', 'EMPLOYEE'] and self.profile_picture:
            return self.profile_picture.url
        return None

    def get_full_address(self):
        if self.is_address_private:
            return None

        address_parts = [
            self.profile_location.name if self.profile_location else None,
            self.profile_city,
            self.profile_address
        ]
        return ", ".join(filter(None, address_parts))

    def get_missing_required_fields(self):
        missing = []

        if self.user.user_type == 'COMPANY':
            if not self.phone_number:
                missing.append("Phone number")
            if not self.company_name:
                missing.append("Company name")

        elif self.user.user_type in ['EMPLOYEE', 'FREELANCER']:
            if not self.public_name:
                missing.append("Public name")
            if not self.profession:
                missing.append("Profession")
            if not self.phone_number:
                missing.append("Phone number")

        return missing

    def __str__(self):
        if self.company_name:
            return self.company_name
        return self.public_name or self.user.email

    @cached_property
    def display_name(self):
        if self.is_contact_private:
            return self.public_name or "N/A"

        match self.user.user_type:
            case UserType.COMPANY:
                return self.company_name or self.public_name or "N/A"
            case UserType.FREELANCER | UserType.EMPLOYEE:
                return self.public_name or "N/A"
            case _:
                return "N/A"


class WorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="work_experiences")

    employer_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    still_there = models.BooleanField(default=False)

    main_tasks = models.TextField(null=True, blank=True)


    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.job_title} at {self.employer_name}"

    def get_duration(self):
        if self.still_there:
            end_date = timezone.now().date()
        else:
            end_date = self.end_date
        return (end_date.year - self.start_date.year) * 12 + end_date.month - self.start_date.month

    def is_current_job(self):
        return self.still_there

class LanguageKnowledge(models.Model):
    language = models.CharField(choices=LanguageChoices.choices)
    level = models.TextField(choices=LanguageKnowledgeLevelChoices.choices)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="languages_known")

    def __str__(self):
        return f"{self.language}"

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="educations")

    school = models.CharField(max_length=255)
    degree = models.ForeignKey(EducationChoice, on_delete=models.CASCADE, related_name="education_degree")
    field_of_study = models.CharField(max_length=255)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    in_progress = models.BooleanField()

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"
        ordering = ['-in_progress', '-start_date', '-end_date']

    def __str__(self):
        return f"{self.school} - {self.degree}"

class CV(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="cvs")
    name = models.CharField(max_length=255, null=True)
    language = models.ForeignKey(LanguageChoice, on_delete=models.SET_NULL, null=True)
    cv_file = models.FileField(upload_to=upload_to_profile_cv_folder)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CoverLetter(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="cover_letters")
    name = models.CharField(max_length=255, null=True)
    language = models.ForeignKey(LanguageChoice, on_delete=models.SET_NULL, null=True)
    cover_letter_file = models.FileField(upload_to=upload_to_profile_cover_letter_folder)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Document(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="documents")
    name = models.CharField(max_length=255, null=True)
    language = models.ForeignKey(LanguageChoice, on_delete=models.SET_NULL, null=True)
    document_file = models.FileField(upload_to=upload_to_profile_document_folder)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

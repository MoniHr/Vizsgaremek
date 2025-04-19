from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.utils.translation import gettext_lazy as _
from apps.job_post.models import (JobPost, JobPostApplication, RequiredLanguageKnowledge, SubCategory)
from apps.profile.models import CV, CoverLetter, DrivingLicenseChoice, EducationChoice, EmploymentScheduleChoice, LocationChoice, WorkingTimeChoice


class RequiredLanguageKnowledgeForm(forms.ModelForm):
    class Meta:
        model = RequiredLanguageKnowledge
        fields = ["language", "level"]

class RequiredLanguageKnowledgeFormset(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data.get("DELETE"):
                continue

            language = form.cleaned_data.get("language")
            level = form.cleaned_data.get("level")

            if not language and not level:
                form.cleaned_data["DELETE"] = True

RequiredLanguageKnowledgeFormset = inlineformset_factory(
    JobPost,
    RequiredLanguageKnowledge,
    form=RequiredLanguageKnowledgeForm,
    formset=RequiredLanguageKnowledgeFormset,
    extra=3,
)

class JobPostForm(forms.ModelForm):
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "tinymce-toolbar",
            "rows": 5,
            "placeholder": "Write the job description here...",
        })
    )

    expectations = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "tinymce-toolbar",
            "rows": 5,
            "placeholder": "Write the expectations here...",
        })
    )

    advantages = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "tinymce-toolbar",
            "rows": 5,
            "placeholder": "Write the advantages here...",
        })
    )

    benefits = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "tinymce-toolbar",
            "rows": 5,
            "placeholder": "Write the benefits here...",
        })
    )

    job_location = forms.ModelChoiceField(
        queryset=LocationChoice.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            "class": "js-select2 select2-hidden-accessible",
            "data-placeholder": "Select Location...",
        })
    )

    educations = forms.ModelMultipleChoiceField(
        queryset=EducationChoice.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={
            "class": "js-select2 select2-hidden-accessible",
            "data-placeholder": "Select required educations...",
        })
    )

    driving_license = forms.ModelMultipleChoiceField(
        queryset=DrivingLicenseChoice.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "js-select2 select2-hidden-accessible",
            "data-placeholder": "Select driving license types...",
        })
    )

    working_time = forms.ModelMultipleChoiceField(
        queryset=WorkingTimeChoice.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={
            "class": "js-select2 select2-hidden-accessible",
            "data-placeholder": "Select working time...",
        })
    )

    work_schedule = forms.ModelMultipleChoiceField(
        queryset=EmploymentScheduleChoice.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={
            "class": "js-select2 select2-hidden-accessible",
            "data-placeholder": "Select work schedule...",
        })
    )

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        NON_REQUIRED_FIELDS = [
            "driving_license", "advantages","job_location", "job_city", "job_address",
            "is_cv_required", "is_cover_letter_required",
            "is_active", "sub_category", "job_description", "expectations", "benefits",
        ]

        for field_name, field in self.fields.items():
            field.required = field_name not in NON_REQUIRED_FIELDS

        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["sub_category"].queryset = SubCategory.objects.filter(category_id=category_id).order_by("name")
            except (ValueError, TypeError):
                self.fields["sub_category"].queryset = SubCategory.objects.none()
        elif self.instance.pk and self.instance.category:
            self.fields["sub_category"].queryset = self.instance.category.subcategories.order_by("name")
        else:
            self.fields["sub_category"].queryset = SubCategory.objects.none()

    class Meta:
        model = JobPost
        fields = (
            "title", "category", "sub_category","job_location", "job_city", "job_address", "job_description", "expectations",
            "educations", "driving_license", "advantages", "working_time",
            "work_schedule",
            "benefits", "is_cv_required", "is_cover_letter_required",
        )


    def clean_job_description(self):
        job_description = self.cleaned_data.get("job_description")
        if not job_description:
            raise forms.ValidationError("Job description is required before submitting.")
        return job_description

    def clean_expectations(self):
        expectations = self.cleaned_data.get("expectations")
        if not expectations:
            raise forms.ValidationError("Expectations are required before submitting.")
        return expectations

    def clean_advantages(self):
        advantages = self.cleaned_data.get("advantages")
        if not advantages:
            raise forms.ValidationError("Advantages are required before submitting.")
        return advantages

    def clean_benefits(self):
        benefits = self.cleaned_data.get("benefits")
        if not benefits:
            raise forms.ValidationError("Benefits are required before submitting.")
        return benefits

    def save(self, commit=True):
        """ M2M mezők megfelelő mentése """
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class ApplyJobForm(forms.ModelForm):
    confirm_submission = forms.BooleanField(
        required=True,
        label="Confirmation",
        help_text="I confirm that I am submitting my application with valid information in my CV and Cover Letter (if required).",
    )

    cv_id = forms.ModelChoiceField(
        queryset=CV.objects.none(),
        required=False,
        label="Select CV",
        empty_label="No CV selected",
    )

    cover_letter_id = forms.ModelChoiceField(
        queryset=CoverLetter.objects.none(),
        required=False,
        label="Select Cover Letter",
        empty_label="No Cover Letter selected",
    )

    class Meta:
        model = JobPostApplication
        fields = ["cv_id", "cover_letter_id", "text", "confirm_submission"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "tinymce-toolbar",
                    "rows": 5,
                    "placeholder": "Write your application message here...",
                }
            ),
        }

    def __init__(self, request, job, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["text"].required = False
        self.fields["cv_id"].queryset = CV.objects.filter(profile__user=request.user)
        self.fields["cover_letter_id"].queryset = CoverLetter.objects.filter(profile__user=request.user)

        # Dinamikus CV mező kezelése
        if job.is_cv_required:
            self.fields["cv_id"].required = True
        else:
            self.fields.pop("cv_id")

        # Dinamikus Cover Letter mező kezelése
        if job.is_cover_letter_required:
            self.fields["cover_letter_id"].required = True
        else:
            self.fields.pop("cover_letter_id")

class EmailJobForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Full name")}),
        label=_("Full name"),
    )
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Email address")}),
        label=_("Email address"),
    )
    subject = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Subject")}),
        label=_("Subject"),
    )
    message = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": _("Message"), "rows": 5}),
        label=_("Message"),
    )
    privacy_policy = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "id": "privacyPolicy"}),
        label=_("I accept the privacy policy"),
    )

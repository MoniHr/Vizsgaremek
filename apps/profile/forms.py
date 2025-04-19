from django import forms
from django.core.exceptions import ValidationError
from django.forms import CheckboxInput, SelectMultiple, Textarea, TextInput
from django.utils.translation import gettext_lazy as _
from apps.core.choices import LanguageChoices, LanguageKnowledgeLevelChoices
from apps.core.forms import (
    BaseHelper,
    HelperWithoutSubmitAndFormTags,
    validate_international_phone_number,
)
from apps.profile.models import CV, Activity, CoverLetter, Document, Education, EducationChoice, LocationChoice, NumberOfWorkerChoice, Profile, SubActivity, WorkExperience
from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()


class CompanyProfileForm(forms.ModelForm):
    helper = BaseHelper()

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        optional_fields = [
            "website", "headquarters", "company_information", "introduction", "sub_activity",
            "year_of_foundation", "number_of_worker", "is_address_private",
            "job_location", "profile_location", "profile_city", "profile_address"
        ]

        for field_name, field in self.fields.items():
            if field_name not in optional_fields:
                field.required = True

        self.fields["phone_number"].validators += (validate_international_phone_number,)

        self.fields["activity"] = forms.ModelChoiceField(
            queryset=Activity.objects.all(),
            widget=forms.Select(attrs={
                "class": "js-select2 select2-hidden-accessible",
                "data-placeholder": "Select main activity...",
                "data-search": "on"
            }),
            required=False
        )

        self.fields["sub_activity"] = forms.ModelChoiceField(
            queryset=SubActivity.objects.none(),  # JS betölti
            widget=forms.Select(attrs={
                "class": "js-select2 select2-hidden-accessible",
                "data-placeholder": "Select sub-activity...",
                "data-search": "on"
            }),
            required=False
        )

        self.fields["profile_location"] = forms.ModelChoiceField(
            queryset=LocationChoice.objects.all(),
            widget=forms.Select(attrs={
                "class": "js-select2 select2-hidden-accessible",
                "data-placeholder": "Select profile location...",
                "data-search": "on"
            }),
            required=False
        )

        # self.fields["profile_city"].widget.attrs.update({
        #     "autocomplete": "new-password",
        #     "placeholder": "Start typing a city name..."
        # })

        # self.fields["profile_address"].widget.attrs.update({
        #     "autocomplete": "new-password",
        #     "placeholder": "Start typing a city name..."
        # })

        self.fields["job_location"] = forms.ModelMultipleChoiceField(
            queryset=LocationChoice.objects.all(),
            widget=forms.SelectMultiple(attrs={
                "class": "js-select2 select2-hidden-accessible",
                "data-placeholder": "Select job location(s)..."
            }),
            required=False
        )

        self.fields["number_of_worker"] = forms.ModelChoiceField(
            queryset=NumberOfWorkerChoice.objects.all(),
            widget=forms.Select(attrs={
                "class": "js-select2 select2-hidden-accessible",
                "data-placeholder": "Select number of workers...",
                "data-search": "on"
            }),
            required=False
        )

        self.fields["internal_communication_languages"].widget.attrs.update({
            "class": "js-select2 select2-hidden-accessible",
            "data-placeholder": "Select internal communication languages...",
            "data-search": "on"
        })

        if instance and instance.pk:
            self.fields["internal_communication_languages"].initial = instance.internal_communication_languages.all()
            self.fields["job_location"].initial = instance.job_location.all()

        self.fields["company_information"].widget.attrs.update({
            "class": "form-control tinymce-toolbar",
            "placeholder": "Write about your company here..."
        })

        self.fields["introduction"].widget.attrs.update({
            "class": "form-control tinymce-toolbar",
            "placeholder": "Write an introduction here..."
        })

    class Meta:
        model = Profile
        widgets = {"is_address_private": forms.CheckboxInput}
        fields = (
            "company_name",
            "company_information",
            "introduction",
            "activity",
            "sub_activity",
            "phone_number",
            "company_email",
            "website",
            "number_of_worker",
            "headquarters",
            "profile_location",
            "profile_city",
            "profile_address",
            "is_address_private",
            "year_of_foundation",
            "internal_communication_languages",
            "job_location"
        )

        labels = {
            "company_name": _("Company Name"),
            "company_information": _("About Us"),
            "phone_number": _("Phone Number"),
            "sub_activity": _("Subactivity"),
            "profile_location": _("Company Location"),
            "profile_city": _("City"),
            "profile_address": _("Address"),
            "headquarters": _("Headquarters"),
            "year_of_foundation": _("Year of Foundation"),
            "number_of_worker": _("Number of Workers"),
            "internal_communication_languages": _("Internal Communication Languages"),
            "website": _("Website"),
            "activity": _("Activity"),
            "introduction": _("Introduction"),
            "is_address_private": _("Is your address private"),
            "company_email": _("Company Email"),
            "job_location": _("Job Location(s)"),
        }

        help_texts = {
            "phone_number": _("Phone number should be in the format +36301231234"),
        }

    def clean_company_information(self):
        company_info = self.cleaned_data.get("company_information")
        if not company_info:
            raise forms.ValidationError("Company Information is required before submitting.")
        return company_info

    # def clean_introduction(self):
    #     introduction = self.cleaned_data.get("introduction")
    #     if not introduction:
    #         raise forms.ValidationError("Introduction is required before submitting.")
    #     return introduction

class EmployeeProfileForm(forms.ModelForm):

    profile_location = forms.ModelChoiceField(
        queryset=LocationChoice.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            "class": "js-select2 select2-hidden-accessible",
            "data-placeholder": "Select Location...",
            "data-search": "on"
        })
    )

    date_of_birth = forms.DateField(
        input_formats=["%Y-%m-%d", "%d.%m.%Y", "%Y.%m.%d", "%m/%d/%Y", "%d/%m/%Y", "%m/%d/%y"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "class": "form-control flatpickr-date",
                "placeholder": "YYYY-MM-DD, DD.MM.YYYY vagy MM/DD/YYYY",
                "autocomplete": "off",
            }
        ),
    )

    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        required_fields = [
            "public_name", "profession", "job_location", "date_of_birth",
            "phone_number", "profile_location", "profile_city", "profile_address"
        ]
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True

        self.fields["phone_number"].validators += (validate_international_phone_number,)

        # self.fields["profile_city"].widget.attrs.update({
        #     "autocomplete": "new-password",
        #     "placeholder": "Start typing a city name..."
        # })

        # self.fields["profile_address"].widget.attrs.update({
        #     "autocomplete": "new-password",
        #     "placeholder": "Start typing a city name..."
        # })

        if instance and instance.pk:
            self.fields["job_location"].initial = instance.job_location.all()
            self.fields["driving_license"].initial = instance.driving_license.all()
            self.fields["working_time"].initial = instance.working_time.all()
            self.fields["work_schedule"].initial = instance.work_schedule.all()

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")
        if date_of_birth:
            today = timezone.now().date()
            age = today.year - date_of_birth.year - (
                (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
            )
            if age < 16:
                raise ValidationError(_("You must be older than 16 years to register"))
        return date_of_birth

    # def clean_introduction(self):
    #     introduction = self.cleaned_data.get("introduction")
    #     if not introduction:
    #         raise forms.ValidationError("Introduction is required before submitting.")
    #     return introduction

    class Meta:
        model = Profile

        fields = (
            "public_name",
            "is_contact_private",
            "profession",
            "job_location",
            "date_of_birth",
            "is_date_of_birth_private",
            "phone_number",
            "is_contact_phone_private",
            "experience",
            "qualification",
            "achievement",
            "introduction",
            "profile_location",
            "profile_city",
            "profile_address",
            "is_address_private",
            "driving_license",
            "working_time",
            "work_schedule",
        )

        widgets = {
            "is_date_of_birth_private": CheckboxInput,
            "is_contact_private": CheckboxInput,
            "is_address_private": CheckboxInput,
            "is_contact_phone_private": CheckboxInput,
            "public_name": TextInput(attrs={"autocomplete": "new-password"}),
            "company_name": TextInput(attrs={"autocomplete": "new-password"}),
            "job_location": SelectMultiple(attrs={"class": "js-select2", "data-placeholder": "Select job locations..."}),
            "introduction": Textarea(attrs={"class": "tinymce-toolbar"}),
            "phone_number": TextInput(attrs={"autocomplete": "new-password"}),
            "experience": TextInput(),
            "qualification": TextInput(),
            "achievement": TextInput(),
            "driving_license": SelectMultiple(attrs={"class": "js-select2", "data-placeholder": "Select driving license types..."}),
            "working_time": SelectMultiple(attrs={"class": "js-select2", "data-placeholder": "Select working times..."}),
            "work_schedule": SelectMultiple(attrs={"class": "js-select2", "data-placeholder": "Select work schedules..."}),
        }

        labels = {
            "public_name": _("Full name"),
            "date_of_birth": _("Date of birth"),
            "is_date_of_birth_private": _("Is date of birth private"),
            "phone_number": _("Phone number"),
            "is_contact_phone_private": _("Is your phone number data private"),
            "profile_city": _("City"),
            "profile_address": _("Address"),
            "profile_location": _("Postcode"),
            "is_address_private": _("Is your address private"),
            "driving_license": _("Driving license"),
            "working_time": _("Working time"),
            "work_schedule": _("Work schedule"),
            "experience": _("Experience"),
            "qualification": _("Qualification"),
            "achievement": _("Achievement"),
            "introduction": _("Introduction"),
            "profession": _("Profession"),
            "job_location": _("Job location"),
        }

        help_texts = {
            "phone_number": _("Phone number should be in the format +36301231234"),
            "is_address_private": _("If your address is private, it will not be visible on the profile."),
            "is_contact_private": _("If is private, it will be hidden, so only your Contact name will appear in chats."),
        }



class CreateLanguageKnowledgeForm(forms.Form):
    language = forms.ChoiceField(
        choices=LanguageChoices.choices,
        widget=forms.Select(attrs={
            "class": "js-select2 select2-hidden-accessible",
            "data-placeholder": "Select language...",
            "data-search": "on"
        })
    )

    level = forms.ChoiceField(
        choices=LanguageKnowledgeLevelChoices.choices,
        widget=forms.Select(attrs={
            "class": "js-select2 select2-hidden-accessible",
            "data-placeholder": "Select language level...",
            "data-search": "on"
        })
    )

class WorkExperienceForm(forms.ModelForm):

    helper = HelperWithoutSubmitAndFormTags()

    class Meta:
        model = WorkExperience
        fields = (
            "employer_name",
            "job_title",
            "start_date",
            "end_date",
            "still_there",
            "main_tasks",
        )
        labels = {
            "employer_name": _("Employer Name"),
            "job_title": _("Job Title"),
            "start_date": _("Start Date"),
            "end_date": _("End Date"),
            "still_there": _("Still here"),
            "main_tasks": _("Main tasks, duties, responsibilities"),
        }
        widgets = {
            "start_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control flatpickr-date",
                    "placeholder": _("YYYY-MM-DD"),
                    "autocomplete": "off",
                }
            ),
            "end_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control flatpickr-date",
                    "placeholder": _("YYYY-MM-DD"),
                    "autocomplete": "off",
                }
            ),
            "main_tasks": forms.Textarea(
                attrs={
                    "class": "form-control tinymce-toolbar",
                    "rows": 4,
                    "placeholder": _("Describe your main tasks..."),
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # Dátumok ellenőrzése
        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError(_("End date must be after start date"))
            cleaned_data["still_there"] = False
        elif start_date and not end_date:
            cleaned_data["still_there"] = True

        return cleaned_data

class EducationForm(forms.ModelForm):
    helper = HelperWithoutSubmitAndFormTags()

    class Meta:
        model = Education
        fields = (
            "school",
            "degree",
            "field_of_study",
            "start_date",
            "end_date",
            "in_progress",
        )
        labels = {
            "school": _("Name of the School"),
            "degree": _("Degree"),
            "field_of_study": _("Field of Study"),
            "start_date": _("Start Date"),
            "end_date": _("End Date"),
            "in_progress": _("In progress"),
        }
        widgets = {
            "school": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("Enter school name"),
            }),
            "field_of_study": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("Enter field of study"),
            }),
            "start_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control flatpickr-date",
                    "placeholder": _("YYYY-MM-DD"),
                    "autocomplete": "off",
                }
            ),
            "end_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control flatpickr-date",
                    "placeholder": _("YYYY-MM-DD"),
                    "autocomplete": "off",
                }
            ),
            "in_progress": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # degree mező override
        self.fields["degree"] = forms.ModelChoiceField(
            queryset=EducationChoice.objects.all(),
            widget=forms.Select(attrs={
                "class": "js-select2 select2-hidden-accessible",
                "data-placeholder": _("Select degree..."),
                "data-search": "on"
            }),
            required=False
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError(_("End date must be after start date"))
            cleaned_data["in_progress"] = False
        elif start_date and not end_date:
            cleaned_data["in_progress"] = True

        return cleaned_data

# class CVForm(forms.ModelForm):
#     helper = HelperWithoutSubmitAndFormTags()
#     cv_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept': '.pdf, image/*'}))

#     class Meta:
#         model = CV
#         fields = ["name", "language", "cv_file", "is_public"]
#         labels = {
#             "name": _("File Name"),
#             "cv_file": _("Upload CV"),
#             "is_public": _("Public?"),
#         }
        

#     def clean(self):
#         cleaned_data = super().clean()
#         name = cleaned_data.get("name")
#         cv_file = cleaned_data.get("cv_file")

#         if not cv_file:
#             raise ValidationError(_("This field is required."))

#         valid_mime_types = ['application/pdf', 'image/jpeg', 'image/png']
#         if cv_file.content_type not in valid_mime_types:
#             raise ValidationError(_("Only PDF and image files (JPEG, PNG) are allowed."))

#         return cleaned_data

class CVForm(forms.ModelForm):
    helper = HelperWithoutSubmitAndFormTags()
    cv_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf, image/*'})
    )

    class Meta:
        model = CV
        fields = ["name", "language", "cv_file", "is_public"]
        labels = {
            "name": _("File Name"),
            "cv_file": _("Upload CV"),
            "is_public": _("Public?"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Select2 styling and attributes to the language field
        self.fields["language"].widget.attrs.update({
            "class": "js-select2 select2-hidden-accessible",
            "data-search": "on",
            "data-placeholder": _("Select language...")
        })

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        cv_file = cleaned_data.get("cv_file")

        if not cv_file:
            raise ValidationError(_("This field is required."))

        valid_mime_types = ['application/pdf', 'image/jpeg', 'image/png']
        if cv_file.content_type not in valid_mime_types:
            raise ValidationError(_("Only PDF and image files (JPEG, PNG) are allowed."))

        return cleaned_data

# class CVEditForm(forms.ModelForm):
#     helper = HelperWithoutSubmitAndFormTags()

#     class Meta:
#         model = CV
#         fields = ["name", "language",  "is_public"]
#         labels = {
#             "name": _("File Name"),
#             "is_public": _("Public?"),
#         }

class CVEditForm(forms.ModelForm):
    helper = HelperWithoutSubmitAndFormTags()

    class Meta:
        model = CV
        fields = ["name", "language", "is_public"]
        labels = {
            "name": _("File Name"),
            "is_public": _("Public?"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Select2 widget with custom attributes to the 'language' field
        self.fields["language"].widget.attrs.update({
            "class": "js-select2 select2-hidden-accessible",
            "data-search": "on",
            "data-placeholder": _("Select language...")
        })

# class CoverLetterForm(forms.ModelForm):
#     helper = HelperWithoutSubmitAndFormTags()
#     cover_letter_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept': '.pdf, image/*'}))

#     class Meta:
#         model = CoverLetter
#         fields = ["name", "language",  "cover_letter_file", "is_public"]
#         labels = {
#             "name": _("Name"),
#             "cover_letter_file": _("Upload Cover Letter"),
#             "is_public": _("Public?"),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         name = cleaned_data.get("name")
#         cover_letter_file = cleaned_data.get("cover_letter_file")

#         if not cover_letter_file:
#             raise ValidationError(_("This field is required."))

#         valid_mime_types = ['application/pdf', 'image/jpeg', 'image/png']
#         if cover_letter_file.content_type not in valid_mime_types:
#             raise ValidationError(_("Only PDF and image files (JPEG, PNG) are allowed."))

#         return cleaned_data

class CoverLetterForm(forms.ModelForm):
    helper = HelperWithoutSubmitAndFormTags()
    cover_letter_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf, image/*'})
    )

    class Meta:
        model = CoverLetter
        fields = ["name", "language", "cover_letter_file", "is_public"]
        labels = {
            "name": _("Name"),
            "cover_letter_file": _("Upload Cover Letter"),
            "is_public": _("Public?"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Select2 attributes to the 'language' field
        self.fields["language"].widget.attrs.update({
            "class": "js-select2 select2-hidden-accessible",
            "data-search": "on",
            "data-placeholder": _("Select language...")
        })

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        cover_letter_file = cleaned_data.get("cover_letter_file")

        if not cover_letter_file:
            raise ValidationError(_("This field is required."))

        valid_mime_types = ['application/pdf', 'image/jpeg', 'image/png']
        if cover_letter_file.content_type not in valid_mime_types:
            raise ValidationError(_("Only PDF and image files (JPEG, PNG) are allowed."))

        return cleaned_data

# class CoverLetterEditForm(forms.ModelForm):
#     helper = HelperWithoutSubmitAndFormTags()

#     class Meta:
#         model = CoverLetter
#         fields = ["name", "language",  "is_public"]
#         labels = {
#             "name": _("Name"),
#             "is_public": _("Public?"),
#         }

class CoverLetterEditForm(forms.ModelForm):
    helper = HelperWithoutSubmitAndFormTags()

    class Meta:
        model = CoverLetter
        fields = ["name", "language", "is_public"]
        labels = {
            "name": _("Name"),
            "is_public": _("Public?"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Select2 styling to the 'language' field
        self.fields["language"].widget.attrs.update({
            "class": "js-select2 select2-hidden-accessible",
            "data-search": "on",
            "data-placeholder": _("Select language...")
        })

class CompanySelectionForm(forms.Form):
    helper = HelperWithoutSubmitAndFormTags()
    company = forms.ModelChoiceField(queryset=User.objects.filter(user_type='COMPANY'),label="Please select company",empty_label="Please select company"),
    widget=forms.Select(attrs={
                "class": "js-select2 select2-hidden-accessible",
                "data-placeholder": "Select company...",
                "data-search": "on"
            }),

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        queryset = User.objects.filter(user_type='COMPANY').exclude(profile=None).select_related('profile')

        if user and hasattr(user, 'profile'):
            blocked_companies = user.profile.blocked_companies.all()
            queryset = queryset.exclude(id__in=blocked_companies.values_list('id', flat=True))

        self.fields['company'].queryset = queryset
        self.fields['company'].label_from_instance = self.get_label_from_instance

    def get_label_from_instance(self, obj):
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.company_name or obj.email
        return obj.email

# class DocumentForm(forms.ModelForm):
#     helper = HelperWithoutSubmitAndFormTags()
#     document_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept': '.pdf, image/*'}))

#     class Meta:
#         model = Document
#         fields = ["name", "language",  "document_file", "is_public"]
#         labels = {
#             "name": _("Name"),
#             "document_file": _("Upload Document"),
#             "is_public": _("Public?"),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         document_file = cleaned_data.get("document_file")
#         name = cleaned_data.get("name")

#         if not document_file:
#             raise ValidationError(_("This field is required."))

#         valid_mime_types = ['application/pdf', 'image/jpeg', 'image/png']
#         if document_file.content_type not in valid_mime_types:
#             raise ValidationError(_("Only PDF and image files (JPEG, PNG) are allowed."))

#         return cleaned_data

class DocumentForm(forms.ModelForm):
    helper = HelperWithoutSubmitAndFormTags()
    document_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf, image/*'})
    )

    class Meta:
        model = Document
        fields = ["name", "language", "document_file", "is_public"]
        labels = {
            "name": _("Name"),
            "document_file": _("Upload Document"),
            "is_public": _("Public?"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Select2 styling to the 'language' field
        self.fields["language"].widget.attrs.update({
            "class": "js-select2 select2-hidden-accessible",
            "data-search": "on",
            "data-placeholder": _("Select language...")
        })

    def clean(self):
        cleaned_data = super().clean()
        document_file = cleaned_data.get("document_file")
        name = cleaned_data.get("name")

        if not document_file:
            raise ValidationError(_("This field is required."))

        valid_mime_types = ['application/pdf', 'image/jpeg', 'image/png']
        if document_file.content_type not in valid_mime_types:
            raise ValidationError(_("Only PDF and image files (JPEG, PNG) are allowed."))

        return cleaned_data

# class DocumentEditForm(forms.ModelForm):
#     helper = HelperWithoutSubmitAndFormTags()

#     class Meta:
#         model = Document
#         fields = ["name", "language",  "is_public"]
#         labels = {
#             "name": _("Name"),
#             "is_public": _("Public?"),
#         }

class DocumentEditForm(forms.ModelForm):
    helper = HelperWithoutSubmitAndFormTags()

    class Meta:
        model = Document
        fields = ["name", "language", "is_public"]
        labels = {
            "name": _("Name"),
            "is_public": _("Public?"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Select2 styling to the 'language' field
        self.fields["language"].widget.attrs.update({
            "class": "js-select2 select2-hidden-accessible",
            "data-search": "on",
            "data-placeholder": _("Select language...")
        })


class EmailForm(forms.Form):
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




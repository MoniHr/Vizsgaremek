import django_filters
from django.db.models import Q
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from django import forms
from apps.accounts.models import UserType
from apps.job_post.models import Category, JobPost, SubCategory
from apps.profile.models import Activity, EducationChoice, LanguageChoice, NumberOfWorkerChoice, Profile, EmploymentScheduleChoice, DrivingLicenseChoice, SubActivity, WorkingTimeChoice, LocationChoice

class EmployeeFilter(django_filters.FilterSet):

    required_language_knowledge_filter = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="languages_known__language",
        queryset=LanguageChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    education = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="educations__degree",
        queryset=EducationChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    public_name = django_filters.CharFilter(
        method="public_name_filter",
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search by name'})
    )

    profile_location = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="profile_location",
        queryset=LocationChoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    work_schedule = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="work_schedule",
        queryset=EmploymentScheduleChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    driving_license = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="driving_license",
        queryset=DrivingLicenseChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    working_time = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="working_time",
        queryset=WorkingTimeChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    job_location = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="job_location",
        queryset=LocationChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = Profile
        fields = []

    def public_name_filter(self, queryset, name, value):
        return queryset.filter(Q(public_name__trigram_similar=value))


    @property
    def qs(self):
        # qs = (
        #     super()
        #     .qs.select_related("user")
        #     .prefetch_related("languages_known", "educations")
        # )

        qs = (
            super()
            .qs.select_related("user")
            .prefetch_related("languages_known", "educations")
        ).filter(public_name__isnull=False)



        if self.request.user.is_authenticated:
            company = self.request.user.company
            if company:
                qs = qs.exclude(blocked_companies=company)
        return qs.filter(user__user_type__in=[UserType.EMPLOYEE]).order_by("pk")


        # return qs.filter(user__user_type__in=[UserType.EMPLOYEE]).order_by("pk")
    # original return qs.filter(user__user_type__in=[UserType.EMPLOYEE, UserType.FREELANCER]).order_by("pk")

class CompanyFilter(django_filters.FilterSet):

    company_name = django_filters.CharFilter(
        method="company_name_filter",
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search by company name'})
    )

    profile_location = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="profile_location",
        queryset=LocationChoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    activity = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="activity",
        queryset=Activity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    sub_activity = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="sub_activity",
        queryset=SubActivity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    number_of_worker = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="number_of_worker",
        queryset=NumberOfWorkerChoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


    class Meta:
        model = Profile
        fields = {"company_name": ["trigram_similar"]}


    def company_name_filter(self, queryset, name, value):
        return queryset.filter(Q(company_name__trigram_similar=value))

    @property
    def qs(self):
        qs = super().qs.select_related("user")
        if self.request.user.is_authenticated:
            company = self.request.user.company
            if company:
                qs = qs.exclude(blocked_companies=company, company_name__isnull=False)
        return qs.filter(user__user_type__in=[UserType.COMPANY])
    # return qs.filter(user__user_type__in=[UserType.COMPANY, UserType.FREELANCER])

class FreelancerFilter(django_filters.FilterSet):

    required_language_knowledge_filter = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="languages_known__language",
        queryset=LanguageChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    education = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="educations__degree",
        queryset=EducationChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    public_name = django_filters.CharFilter(
        method="public_name_filter",
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search by name'})
    )

    profile_location = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="profile_location",
        queryset=LocationChoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    work_schedule = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="work_schedule",
        queryset=EmploymentScheduleChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    working_time = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="working_time",
        queryset=WorkingTimeChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    job_location = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="job_location",
        queryset=LocationChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    driving_license = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="driving_license",
        queryset=DrivingLicenseChoice.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = Profile
        fields = []

    def public_name_filter(self, queryset, name, value):
        return queryset.filter(Q(public_name__trigram_similar=value))

    @property
    def qs(self):
        qs = (
            super().qs
            .select_related("user")
            .prefetch_related("languages_known", "educations")
        )

        if self.request.user.is_authenticated:
            company = self.request.user.company
            if company:
                qs = qs.exclude(blocked_companies=company, public_name__isnull=False)
        return qs.filter(user__user_type__in=[UserType.FREELANCER]).order_by("pk")


class JobPostFilter(django_filters.FilterSet):
    required_language_knowledge_filter = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="required_languages__language",
        queryset=LanguageChoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    title = django_filters.CharFilter(
        method="job_title_filter",
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search by Job title'})
    )

    address = django_filters.CharFilter(
        method="address_filter",
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Where'})
    )

    job_location = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="job_location",
        queryset=LocationChoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    education = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="educations",
        queryset=EducationChoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    working_time = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="working_time",
        queryset=WorkingTimeChoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    work_schedule = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="work_schedule",
        queryset=EmploymentScheduleChoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    category = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="category",
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    sub_category = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="sub_category",
        queryset=SubCategory.objects.none(),  # Initially empty, dynamically updated
        widget=forms.CheckboxSelectMultiple,
    )

    driving_license = django_filters.ModelMultipleChoiceFilter(
        label="",
        field_name="driving_license",
        queryset=DrivingLicenseChoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = JobPost
        fields = {
            "benefits": ["istartswith"],
            "advantages": ["istartswith"],
            "job_description": ["istartswith"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamic subcategory filtering based on selected category
        if "category" in self.data:
            try:
                category_ids = self.data.getlist("category")
                self.filters["sub_category"].queryset = SubCategory.objects.filter(category_id__in=category_ids)
            except ValueError:
                pass  # Ignore invalid inputs

    def address_filter(self, queryset, name, value):
        return queryset.filter(
            Q(address__icontains=value)
            | Q(city__icontains=value)
            | Q(country__icontains=value)
            | Q(profile_location__icontains=value)
        )

    def job_title_filter(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value))

    @property
    def qs(self):
        qs = super().qs
        return qs.filter(is_active=True).order_by("-created_at")

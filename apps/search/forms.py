from crispy_forms.layout import HTML, Layout
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML

# Field("education", css_class="form-select"),

class JobSearchHelper(FormHelper):
    def __init__(self):
        super().__init__()
        self.form_method = "GET"
        self.layout = Layout(
            HTML("<h6 class='overline-title text-primary-alt'>Search Job</h6>"),
            Field("title", placeholder="What"),
            # Field("address", placeholder="Where"),

            HTML("<h6 class='overline-title text-primary-alt'>Category</h6>"),
            Field("category"),

            HTML("<h6 class='overline-title text-primary-alt'>Subcategory</h6>"),
            Field("sub_category"),

            HTML("<h6 class='overline-title text-primary-alt'>Job Location</h6>"),
            Field("job_location"),

            HTML("<h6 class='overline-title text-primary-alt'>Education</h6>"),
            Field("education"),

            HTML("<h6 class='overline-title text-primary-alt'>Working Time</h6>"),
            Field("working_time"),

            HTML("<h6 class='overline-title text-primary-alt'>Work Schedule</h6>"),
            Field("work_schedule"),

            HTML("<h6 class='overline-title text-primary-alt'>Driving License</h6>"),
            Field("driving_license"),

            HTML("<h6 class='overline-title text-primary-alt'>Language Knowledge</h6>"),
            Field("required_language_knowledge_filter"),
        )



class CompanySearchHelper(FormHelper):
    def __init__(self):
        super().__init__()
        self.form_method = "GET"
        self.disable_csrf = True
        self.layout = Layout(
            HTML("<h6 class='overline-title text-primary-alt'>Company Details</h6>"),
            Field("company_name", placeholder=_("Enter company name")),
            HTML("<h6 class='overline-title text-primary-alt'>Location</h6>"),
            Field("profile_location"),
            HTML("<h6 class='overline-title text-primary-alt'>Activity Details</h6>"),
            Field("activity"),
            HTML("<h6 class='overline-title text-primary-alt'>Sub Activity</h6>"),
            Field("sub_activity"),
            HTML("<h6 class='overline-title text-primary-alt'>Workforce Information</h6>"),
            Field("number_of_worker"),
        )

class EmployeeSearchHelper(FormHelper):
    def __init__(self):
        super().__init__()
        self.form_method = "GET"
        self.disable_csrf = True
        self.layout = Layout(
            HTML("<h6 class='overline-title text-primary-alt'>Employee Details</h6>"),
            Field("public_name", placeholder=_("Enter name")),
            HTML("<h6 class='overline-title text-primary-alt'>Location</h6>"),
            Field("profile_location"),
            # HTML("<h6 class='overline-title text-primary-alt'>Job Location</h6>"),
            # Field("job_location"),
            HTML("<h6 class='overline-title text-primary-alt'>Education</h6>"),
            Field("education"),
            HTML("<h6 class='overline-title text-primary-alt'>Working Time</h6>"),
            Field("working_time"),
            HTML("<h6 class='overline-title text-primary-alt'>Work Schedule</h6>"),
            Field("work_schedule"),
            HTML("<h6 class='overline-title text-primary-alt'>Driving License</h6>"),
            Field("driving_license"),
            HTML("<h6 class='overline-title text-primary-alt'>Language Knowledge</h6>"),
            Field("required_language_knowledge_filter"),
        )


class FreelancerSearchHelper(FormHelper):
    def __init__(self):
        super().__init__()
        self.form_method = "GET"
        self.disable_csrf = True
        self.layout = Layout(
            HTML("<h6 class='overline-title text-primary-alt'>Freelancer Details</h6>"),
            Field("public_name", placeholder=_("Enter name")),
            HTML("<h6 class='overline-title text-primary-alt'>Location</h6>"),
            Field("profile_location"),
            # HTML("<h6 class='overline-title text-primary-alt'>Job Preferences</h6>"),
            # Field("job_location"),
            HTML("<h6 class='overline-title text-primary-alt'>Education</h6>"),
            Field("education"),
            HTML("<h6 class='overline-title text-primary-alt'>Working Time</h6>"),
            Field("working_time"),
            HTML("<h6 class='overline-title text-primary-alt'>Working Schedule</h6>"),
            Field("work_schedule"),

            HTML("<h6 class='overline-title text-primary-alt'>Driving License</h6>"),
            Field("driving_license"),
            HTML("<h6 class='overline-title text-primary-alt'>Language Knowledge</h6>"),
            Field("required_language_knowledge_filter"),
        )

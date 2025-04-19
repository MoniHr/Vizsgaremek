from django.contrib import admin
from apps.profile.models import CV, Activity, CoverLetter, Document, Education, EmploymentScheduleChoice, LanguageChoice, LanguageKnowledge, NumberOfWorkerChoice, Profile, DrivingLicenseChoice, SubActivity, WorkExperience, WorkingTimeChoice, EducationChoice, LocationChoice
from import_export.admin import ImportExportModelAdmin

from apps.profile.resources import ActivityResource, CVResource, CoverLetterResource, DocumentResource, DrivingLicenseChoiceResource, EducationChoiceResource, EducationResource, EmploymentScheduleChoiceResource, LocationChoiceResource, LanguageChoiceResource, LanguageKnowledgeResource, NumberOfWorkerChoiceResource, ProfileResource, SubActivityResource, WorkExperienceResource, WorkingTimeChoiceResource

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource
    list_display = ("user", "public_name", "profession", "company_name", "is_active")
    search_fields = ("user__email", "public_name", "company_name")
@admin.register(CV)
class CVAdmin(ImportExportModelAdmin):
    resource_class = CVResource
    list_display = ("profile", "name", "language", "created_at", "is_public")
    search_fields = ("name", "profile__public_name")
@admin.register(CoverLetter)
class CoverLetterAdmin(ImportExportModelAdmin):
    resource_class = CoverLetterResource
    list_display = ("profile", "name", "language", "created_at", "is_public")
    search_fields = ("name", "profile__public_name")

@admin.register(Document)
class DocumentAdmin(ImportExportModelAdmin):
    resource_class = DocumentResource
    list_display = ("profile", "name", "language", "created_at", "is_public")
    search_fields = ("name", "profile__public_name")




@admin.register(WorkExperience)
class WorkExperienceAdmin(ImportExportModelAdmin):
    resource_class = WorkExperienceResource
    list_display = ("profile", "employer_name", "job_title", "start_date", "end_date", "still_there")

@admin.register(LanguageKnowledge)
class LanguageKnowledgeAdmin(ImportExportModelAdmin):
    resource_class = LanguageKnowledgeResource
    list_display = ("profile", "language", "level")

@admin.register(Education)
class EducationAdmin(ImportExportModelAdmin):
    resource_class = EducationResource
    list_display = ("profile", "school", "degree", "field_of_study", "start_date", "end_date", "in_progress")

@admin.register(Activity)
class ActivityAdmin(ImportExportModelAdmin):
    resource_class = ActivityResource
    list_display = ("code", "name")

@admin.register(SubActivity)
class SubActivityAdmin(ImportExportModelAdmin):
    resource_class = SubActivityResource
    list_display = ("activity", "code", "name")

@admin.register(LocationChoice)
class LocationChoiceAdmin(ImportExportModelAdmin):
    resource_class = LocationChoiceResource
    list_display = ("code", "name")

@admin.register(NumberOfWorkerChoice)
class NumberOfWorkerChoiceAdmin(ImportExportModelAdmin):
    resource_class = NumberOfWorkerChoiceResource
    list_display = ("code", "name")

@admin.register(EducationChoice)
class EducationChoiceAdmin(ImportExportModelAdmin):
    resource_class = EducationChoiceResource
    list_display = ("code", "name", "custom_order")

@admin.register(LanguageChoice)
class LanguageChoiceAdmin(ImportExportModelAdmin):
    resource_class = LanguageChoiceResource
    list_display = ("code", "name")

@admin.register(EmploymentScheduleChoice)
class EmploymentScheduleChoiceAdmin(ImportExportModelAdmin):
    resource_class = EmploymentScheduleChoiceResource
    list_display = ("code", "name")

@admin.register(DrivingLicenseChoice)
class DrivingLicenseChoiceAdmin(ImportExportModelAdmin):
    resource_class = DrivingLicenseChoiceResource
    list_display = ("code", "name")

@admin.register(WorkingTimeChoice)
class WorkingTimeChoiceAdmin(ImportExportModelAdmin):
    resource_class = WorkingTimeChoiceResource
    list_display = ("code", "name")

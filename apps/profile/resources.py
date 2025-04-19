from import_export import resources
from apps.profile.models import CV, Activity, CoverLetter, Document, DrivingLicenseChoice, Education, EducationChoice, EmploymentScheduleChoice, LocationChoice, LanguageChoice, LanguageKnowledge, NumberOfWorkerChoice, Profile, SubActivity, WorkExperience, WorkingTimeChoice



class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

class CVResource(resources.ModelResource):
    class Meta:
        model = CV

class CoverLetterResource(resources.ModelResource):
    class Meta:
        model = CoverLetter

class DocumentResource(resources.ModelResource):
    class Meta:
        model = Document


class WorkExperienceResource(resources.ModelResource):
    class Meta:
        model = WorkExperience

class LanguageKnowledgeResource(resources.ModelResource):
    class Meta:
        model = LanguageKnowledge

class EducationResource(resources.ModelResource):
    class Meta:
        model = Education

class ActivityResource(resources.ModelResource):
    class Meta:
        model = Activity

class SubActivityResource(resources.ModelResource):
    class Meta:
        model = SubActivity

class LocationChoiceResource(resources.ModelResource):
    class Meta:
        model = LocationChoice

class NumberOfWorkerChoiceResource(resources.ModelResource):
    class Meta:
        model = NumberOfWorkerChoice

class EducationChoiceResource(resources.ModelResource):
    class Meta:
        model = EducationChoice

class LanguageChoiceResource(resources.ModelResource):
    class Meta:
        model = LanguageChoice

class EmploymentScheduleChoiceResource(resources.ModelResource):
    class Meta:
        model = EmploymentScheduleChoice

class DrivingLicenseChoiceResource(resources.ModelResource):
    class Meta:
        model = DrivingLicenseChoice

class WorkingTimeChoiceResource(resources.ModelResource):
    class Meta:
        model = WorkingTimeChoice


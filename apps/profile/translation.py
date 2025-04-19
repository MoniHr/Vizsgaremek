from apps.job_post.models import Category, SubCategory
from modeltranslation.translator import translator, TranslationOptions
from .models import Activity, DrivingLicenseChoice, EducationChoice, EmploymentScheduleChoice, LocationChoice, LanguageChoice, NumberOfWorkerChoice, SubActivity, WorkingTimeChoice

class EmploymentScheduleChoiceTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(EmploymentScheduleChoice, EmploymentScheduleChoiceTranslationOptions)

class LanguageChoiceTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(LanguageChoice, LanguageChoiceTranslationOptions)

class DrivingLicenseChoiceTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(DrivingLicenseChoice, DrivingLicenseChoiceTranslationOptions)

class WorkingTimeChoiceTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(WorkingTimeChoice, WorkingTimeChoiceTranslationOptions)

class EducationChoiceTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(EducationChoice, EducationChoiceTranslationOptions)

class LocationChoiceTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(LocationChoice, LocationChoiceTranslationOptions)


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Category, CategoryTranslationOptions)


class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(SubCategory, SubCategoryTranslationOptions)


class ActivityTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Activity, ActivityTranslationOptions)


class SubActivityTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(SubActivity, SubActivityTranslationOptions)



class NumberOfWorkerChoiceTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(NumberOfWorkerChoice, NumberOfWorkerChoiceTranslationOptions)

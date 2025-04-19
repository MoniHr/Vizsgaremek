from django.contrib import admin
from apps.job_post.models import JobPlan, JobPost, JobPostApplication, Category, SubCategory
from import_export.admin import ImportExportModelAdmin
from apps.job_post.resources import CategoryResource, SubCategoryResource


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('code', 'name', 'featured', 'order')
    search_fields = ('name', 'code')
    list_filter = ('featured',)


@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin):
    resource_class = SubCategoryResource
    list_display = ('code', 'name', 'category')
    search_fields = ('name', 'code')
    list_filter = ('category',)


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = (
        "title", "is_active", "is_boosted", "boost_end_date", "can_edit_title_display",
        "stripe_payment_intent_id", "stripe_customer_email", "created_at"
    )
    list_filter = (
        "is_active", "is_boosted", "boost_location", "created_at"
    )
    search_fields = (
        "title", "job_city", "job_address", "contact_email", "stripe_customer_email", "stripe_payment_intent_id"
    )

    readonly_fields = (
        "slug",
        "boost_start_date",
        "boost_end_date",
        "title_editable_until",
        "expiration_reminder_sent",
        "stripe_payment_intent_id",
        "stripe_checkout_session_id",
        "stripe_transaction_completed_at",
        "stripe_customer_email",
    )

    fieldsets = (
        (None, {
            "fields": ("title", "slug", "is_active", "job_description", "expectations", "advantages", "benefits")
        }),
        ("Boost settings", {
            "fields": (
                "is_boosted", "boost_location", "selected_plan",
                "boost_start_date", "boost_end_date", "title_editable_until", "expiration_reminder_sent"
            ),
            "classes": ("collapse",),
        }),
        ("Location", {
            "fields": ("job_location", "job_city", "job_address")
        }),
        ("Contact", {
            "fields": ("contact_email", "contact_phone")
        }),
        ("Billing", {
            "fields": (
                "billing_name", "billing_tax_number", "billing_address",
                "billing_city", "billing_state", "billing_zip_code", "billing_country"
            ),
            "classes": ("collapse",),
        }),
        ("Stripe Transaction Info", {
            "fields": (
                "stripe_payment_intent_id",
                "stripe_checkout_session_id",
                "stripe_customer_email",
                "stripe_transaction_completed_at",
            ),
            "classes": ("collapse",),
        }),
        ("Advanced", {
            "fields": (
                "category", "sub_category", "educations", "driving_license",
                "working_time", "work_schedule", "is_cv_required", "is_cover_letter_required",
                "saved_by", "created_by"
            ),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Can edit title?")
    def can_edit_title_display(self, obj):
        return obj.can_edit_title()


# admin.site.register(JobPost)
admin.site.register(JobPostApplication)


@admin.register(JobPlan)
class JobPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "plan_type", "duration_days", "price", "is_recommended" ,"is_active")
    list_filter = ("plan_type", "is_active")
    search_fields = ("name", "description")
    ordering = ("price", "duration_days")

    fieldsets = (
        (None, {
            "fields": ("name", "description")
        }),
        ("Plan Settings", {
            "fields": ("plan_type", "duration_days", "price", "is_recommended", "is_active")
        }),
    )

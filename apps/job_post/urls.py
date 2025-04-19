from django.urls import path
from apps.job_post import views
from apps.search.views import job_detail

urlpatterns = [
    path("job/<slug:slug>/", job_detail, name="job_detail"),
    path("my-jobs/", views.list_jobs_view, name="list_jobs"),
    path("create/", views.create_job_post, name="create_job"),
    path("<slug:slug>/edit/", views.edit_job_post, name="job_edit"),
    path("<slug:slug>/delete/", views.delete_job_post, name="job_delete"),

    # Wishlist Routes
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/toggle/<slug:job_slug>/", views.wishlist_toggle, name="wishlist_toggle"),

    # Job Applications
    path("<slug:slug>/apply/", views.job_apply, name="job_apply"),
    path("my-applications/", views.job_my_applications, name="my_applications"),
    path("applications/", views.job_applications, name="applications"),
    path("applications/delete/<int:application_id>/", views.delete_application, name="delete_application"),


    # Boost Job - Stripe Checkout trigger
    path("boost/<slug:slug>/choose-plan/", views.boost_job_post, name="boost_choose_plan"),
    path("boost/<slug:slug>/checkout/", views.stripe_checkout_start, name="boost_checkout"),
    path("boost/<slug:slug>/success/", views.stripe_success, name="boost_success"),

    # Email & AJAX Routes
    path("send-email-job/", views.send_email_job, name="send_email_job"),
    path("ajax/load-sub-categories/", views.load_sub_categories, name="ajax_load_sub_categories"),
]

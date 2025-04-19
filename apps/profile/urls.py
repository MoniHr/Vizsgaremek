from django.urls import path
from django.contrib.auth import views as auth_views

from apps.profile import views

urlpatterns = [
    path("profile/edit/", views.edit_profile_view, name="edit_profile"),
    path("profile/<slug:slug>", views.public_profile, name="public_profile"),

    path("work-experience/", views.list_work_experience, name="list_work_experience"),
    path("work-experience/create/", views.create_work_experience, name="create_work_experience"),
    path("work-experience/<int:pk>/delete/", views.delete_work_experience, name="delete_work_experience"),

    path("education/list/", views.list_education, name="list_education"),
    path("education/create/", views.create_education, name="create_education"),
    path("education/delete/<int:pk>/", views.delete_education, name="delete_education"),


    path("language-knowledge/list/", views.list_language_knowledge, name="list_language_knowledge"),
    path("language-knowledge/create/", views.create_language_knowledge, name="create_language_knowledge"),
    path("language-knowledge/delete/<int:pk>/", views.delete_language_knowledge, name="delete_language_knowledge"),


    path("documents/", views.list_documents, name="list_document"),
    path("document/create/", views.create_document, name="create_document"),
    path("document/edit/<int:pk>/", views.edit_document, name="edit_document"),
    path("document/delete/<int:pk>/", views.delete_document, name="delete_document"),

    path("cv/list/", views.list_cv, name="list_cv"),
    path("cv/create/", views.create_cv, name="create_cv"),
    path("cv/edit/<int:pk>/", views.edit_cv, name="edit_cv"),
    path("cv/delete/<int:pk>/", views.delete_cv, name="delete_cv"),

    path("cover-letters/", views.list_cover_letters, name="list_cover_letter"),
    path("cover-letter/create/", views.create_cover_letter, name="create_cover_letter"),
    path("cover-letter/edit/<int:pk>/", views.edit_cover_letter, name="edit_cover_letter"),
    path("cover-letter/delete/<int:pk>/", views.delete_cover_letter, name="delete_cover_letter"),

    path("blocked-companies/", views.blocked_company_list, name="list_blocked_company"),
    path("blocked-companies/edit/", views.edit_blocked_company, name="edit_blocked_company"),
    path("blocked-company/delete/<int:pk>/", views.delete_blocked_company, name="delete_blocked_company"),

    path("profile/change-image/", views.change_profile_image, name="change_profile_image"),
    path("profile/generate-cv/", views.generate_cv, name="generate_cv"),
    path("ajax/load-sub-activities/", views.load_sub_activities, name="ajax_load_sub_activities"),

    path("send-email/", views.send_email_view, name="send_email"),

    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='dashboard/common/change_password.html'), name='change_password'),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="dashboard/common/password_change_done.html"), name="password_change_done"),

    path("send-test-email/", views.send_simple_email, name="send_simple_email"),

    ]

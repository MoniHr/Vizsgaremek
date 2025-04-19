from django.urls import path
from apps.search import views

urlpatterns = [
    path("employees/", views.search_employees, name="search_employees"),
    path("company/", views.search_companies, name="search_company"),
    path("freelancers/", views.search_freelancers, name="search_freelancers"),
    path("jobs/", views.search_job_posts, name="search_job_posts"),
    path('ajax/load-sub-categories/filter/', views.load_sub_categories_filter, name='ajax_load_sub_categories_filter'),
    path('ajax/load-sub-activities/filter/', views.load_sub_activities_filter, name='ajax_load_sub_activities_filter'),
]

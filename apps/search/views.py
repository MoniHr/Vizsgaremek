from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Prefetch, Q
from apps.job_post.choices import SubIndustryChoicesByIndustry
from apps.job_post.models import JobPost, SubCategory
from apps.profile.forms import EmailForm
from apps.profile.models import SubActivity
from apps.search.filters import CompanyFilter, EmployeeFilter, FreelancerFilter, JobPostFilter
from apps.search.forms import CompanySearchHelper, EmployeeSearchHelper, FreelancerSearchHelper, JobSearchHelper

PAGINATE_BY = 25


def job_detail(request, slug):
    job_post = get_object_or_404(JobPost, slug=slug)
    profile = getattr(request.user, "profile", None) if request.user.is_authenticated else None

    # Ellenőrizzük, hogy a felhasználónak van-e feltöltött CV-je vagy Cover Letter-e
    has_cv = profile and profile.cvs.exists()
    has_cover_letter = profile and profile.cover_letters.exists()

    # Hiányzó dokumentumok listájának létrehozása, csak ha a munka megköveteli
    missing_documents = []
    if job_post.is_cv_required and not has_cv:
        missing_documents.append("CV (Resume)")
    if job_post.is_cover_letter_required and not has_cover_letter:
        missing_documents.append("Cover Letter")

    # Figyelmeztető üzenet és feltöltési linkek
    warning_message = None
    upload_links = []

    if missing_documents:
        warning_message = f"Before applying, please upload the following document(s): {', '.join(missing_documents)}."
        if "CV (Resume)" in missing_documents:
            upload_links.append({"label": "Upload CV", "url": reverse("create_cv"), "class": "btn-primary"})
        if "Cover Letter" in missing_documents:
            upload_links.append({"label": "Upload Cover Letter", "url": reverse("create_cover_letter"), "class": "btn-secondary"})

    # Az "Apply" gomb csak akkor lesz letiltva, ha a munka megköveteli valamelyik dokumentumot, és az hiányzik
    is_apply_disabled = bool(missing_documents)

    # **Adott cég további aktív állásai**
    company_jobs = JobPost.objects.filter(
        created_by=job_post.created_by, is_active=True
    ).exclude(id=job_post.id).select_related("category", "sub_category", "job_location")[:5]

    # **Similar Jobs – azonos kategóriájú vagy alkategóriájú aktív állások**
    similar_jobs = JobPost.objects.filter(
        Q(category=job_post.category) | Q(sub_category=job_post.sub_category),
        is_active=True
    ).exclude(id=job_post.id).exclude(created_by=job_post.created_by).select_related("category", "sub_category", "job_location")[:5]

    context = {
        "job_post": job_post,
        "email_form": EmailForm(),
        "is_apply_disabled": is_apply_disabled,  # Apply gomb disabled állapota
        "warning_message": warning_message,  # Figyelmeztető szöveg
        "upload_links": upload_links,  # Feltöltési linkek listája
        "company_jobs": company_jobs,  # Adott cég aktív állásai
        "similar_jobs": similar_jobs,  # Hasonló állások
    }

    return render(request, "job_post/jobs/detail.html", context)

def search_employees(request):
    f = EmployeeFilter(request.GET, request=request)

    employee_queryset = (
        f.qs
        .filter(is_active=True)
        .select_related("activity", "sub_activity")
        .prefetch_related(
            Prefetch("user__job_posts", queryset=JobPost.objects.select_related("category", "sub_category"))
        )
    )

    paginator = Paginator(employee_queryset, PAGINATE_BY)
    page = request.GET.get("page")

    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/employee.html",
        {
            "filter": f,
            "helper": EmployeeSearchHelper(),
            "page_obj": paginated_objects,
            "request": request,
        },
    )

def search_freelancers(request):
    f = FreelancerFilter(request.GET, request=request)

    freelancer_queryset = (
        f.qs
        .filter(is_active=True)
        .select_related("activity", "sub_activity")
        .prefetch_related(
            Prefetch("user__job_posts", queryset=JobPost.objects.select_related("category", "sub_category"))
        )
    )

    paginator = Paginator(freelancer_queryset, PAGINATE_BY)
    page = request.GET.get("page")

    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/freelancer.html",
        {
            "filter": f,
            "helper": FreelancerSearchHelper(),
            "page_obj": paginated_objects,
            "request": request,
        },
    )

def search_companies(request):
    f = CompanyFilter(request.GET, request=request)

    company_queryset = (
        f.qs
        .filter(is_active=True)
        .select_related("activity", "sub_activity", "number_of_worker")
        .prefetch_related(
            Prefetch("user__job_posts", queryset=JobPost.objects.select_related("category", "sub_category"))
        )
    )

    paginator = Paginator(company_queryset, PAGINATE_BY)
    page = request.GET.get("page")

    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/company.html",
        {
            "filter": f,
            "helper": CompanySearchHelper(),
            "page_obj": paginated_objects,
            "request": request,
        },
    )

def search_job_posts(request):
    f = JobPostFilter(request.GET, request=request)

    job_posts_queryset = (
        f.qs
        .select_related("category", "sub_category", "job_location")  # Egy-a-többhöz kapcsolatok optimalizálása
        .prefetch_related("working_time", "work_schedule")  # Sok-a-sokhoz kapcsolatok optimalizálása
    )

    paginator = Paginator(job_posts_queryset, PAGINATE_BY)
    page = request.GET.get("page")

    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/jobs.html",
        {
            "filter": f,
            "helper": JobSearchHelper(),
            "page_obj": paginated_objects,
            "sub_industries": SubIndustryChoicesByIndustry,
            "request": request,
        },
    )


def load_sub_categories_filter(request):
    category_ids = request.GET.get('category_ids', '')

    if category_ids:
        category_ids = [int(id) for id in category_ids.split(',') if id.isdigit()]
        sub_categories = SubCategory.objects.filter(category_id__in=category_ids).values('id', 'name', 'category_id')
        return JsonResponse(list(sub_categories), safe=False)

    return JsonResponse([], safe=False)

def load_sub_activities_filter(request):
    activity_ids = request.GET.get('activity_ids', '')

    if activity_ids:
        activity_ids = [int(id) for id in activity_ids.split(',') if id.isdigit()]
        sub_activities = SubActivity.objects.filter(activity_id__in=activity_ids).values('id', 'name', 'activity_id')
        return JsonResponse(list(sub_activities), safe=False)

    return JsonResponse([], safe=False)


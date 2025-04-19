
from apps.job_post.models import JobPost, JobPostApplication


def unread_applications_count(request):
    if request.user.is_authenticated:
        count = JobPostApplication.objects.filter(
            job__created_by=request.user,
            is_read=False
        ).count()
    else:
        count = 0
    return {
        "unread_applications_count": count
    }

def active_job_posts_count(request):
    if request.user.is_authenticated:
        count = JobPost.objects.filter(
            created_by=request.user,
            is_active=True
        ).count()
    else:
        count = 0
    return {
        "active_job_posts_count": count
    }

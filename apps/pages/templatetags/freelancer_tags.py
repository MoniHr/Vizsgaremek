from django import template

from apps.accounts.models import UserType
from apps.profile.models import Profile

register = template.Library()


@register.simple_tag()
def top_freelancers():
    return Profile.objects.filter(user__user_type=UserType.FREELANCER).order_by("pk")[
        0:5
    ]


@register.simple_tag()
def featured_freelancers():
    return Profile.objects.filter(user__user_type=UserType.FREELANCER).order_by("pk")[
        0:5
    ]

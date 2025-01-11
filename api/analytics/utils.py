from .models import AnalyticProfileViews, Analytic
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from api.profile_user.models import Profile

def log_profile_view(slug):

    now = datetime.now()
    month = now.month
    year = now.year

    analytic, _ = Analytic.objects.get_or_create(
        route=slug,
        month=month,
        year=year
    )

    try:
            
        profile = Profile.objects.get(slug=slug)

        profile_view = AnalyticProfileViews.objects.get(owner__pk=profile.by.pk)

        profile_view.number += 1
        profile_view.save()

    except ObjectDoesNotExist:

        raise ValueError(f"Usuário com o slug '{slug}' não encontrado.")

    return analytic, profile_view

from .models import AnalyticProfileViews, Analytic
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from api.profile_user.models import Profile

from django.conf import settings
from geopy.geocoders import Nominatim
import requests

DEBUG = settings.DEBUG

def get_location_from_ip(ip_address):

    try:

        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        data = response.json()

        return data.get('city', 'Localização desconhecida')
    
    except Exception:

        return 'Localização desconhecida'

def log_profile_view(request, slug):

    now = datetime.now()
    month = now.month
    year = now.year

    referrer_link = request.META.get('HTTP_REFERER', '')

    current_path = (
        f'https://cliquenabio.vercel.app{request.get_full_path()}' if not DEBUG else f'http://127.0.0.1:8000{request.get_full_path()}'
    )

    referrer_link = f'{referrer_link}{current_path}' if referrer_link else f'Direto ({current_path})'

    device_type = request.META.get('HTTP_USER_AGENT', 'Desconhecido')
    ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')

    location = get_location_from_ip(ip_address)

    analytic, _ = Analytic.objects.get_or_create(
        route=slug,
        month=month,
        year=year
    )

    try:
            
        profile = Profile.objects.get(slug=slug)

        profile_view = AnalyticProfileViews.objects.get(
            owner__pk=profile.by.pk,
        )

        profile_view.number += 1
        profile_view.save(
            referrer_link=referrer_link,
            device_type=device_type,
            location=location
        )

    except ObjectDoesNotExist:

        raise ValueError(f"Usuário com o slug '{slug}' não encontrado.")

    return analytic, profile_view

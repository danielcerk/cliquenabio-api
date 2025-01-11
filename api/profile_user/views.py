from django.shortcuts import render, get_object_or_404

from api.analytics.utils import log_profile_view
from .models import Profile

from rest_framework.permissions import (

    AllowAny

)
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileDetailView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, slug):

        profile = get_object_or_404(Profile, slug=slug)

        user = User.objects.get(pk=profile.by.pk)

        log_profile_view(slug)

        return Response({
            "id": user.id,
            "name": user.name,
            "full_name": user.full_name,
            "email": user.email,
            "slug": profile.slug,
            "biografy": profile.biografy,
        })
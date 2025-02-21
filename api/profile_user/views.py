from django.shortcuts import render, get_object_or_404

from api.links.models import Link
from api.links.serializers import LinkSerializer
from api.snaps.models import Snap
from api.snaps.serializers import SnapSerializer
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

        links = Link.objects.filter(created_by=user).all().order_by('-created_at')
        link_serializer = LinkSerializer(instance=links, many=True)

        snaps = Snap.objects.filter(created_by=user).all().order_by('-created_at')
        snap_serializer = SnapSerializer(instance=snaps, many=True)

        log_profile_view(request, slug)

        return Response({
            "id": user.id,
            "name": user.name,
            "full_name": user.full_name,
            "email": user.email,
            "slug": profile.slug,
            "biografy": profile.biografy,
            "links": link_serializer.data,
            "snaps": snap_serializer.data,
        })
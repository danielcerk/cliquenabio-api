from django.shortcuts import render, get_object_or_404

from api.form_contact.models import FormContactEmail
from api.subscriptions.models import Subscription
from api.links.models import Link
from api.links.serializers import LinkSerializer
from api.snaps.models import Snap
from api.snaps.serializers import SnapSerializer
from api.analytics.utils import log_profile_view
from .models import Profile
from api.notes.models import Note  
from api.notes.serializers import NoteSerializer  

from api.theme.models import ThemeUser, ThemeGlobal  # Importe os modelos de tema
from api.theme.serializers import ThemeGlobalSerializer  # Importe o serializer do tema

from rest_framework.permissions import (

    AllowAny, IsAuthenticated

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

        get_user_plan = Subscription.objects.get(user=user)

        links = Link.objects.filter(created_by=user).all().order_by('-created_at')
        link_serializer = LinkSerializer(instance=links, many=True)

        snaps = Snap.objects.filter(created_by=user).all().order_by('-created_at')
        snap_serializer = SnapSerializer(instance=snaps, many=True)

        notes = Note.objects.filter(user=user).all().order_by('-created_at')
        note_serializer = NoteSerializer(instance=notes, many=True)

        # Busca o tema do usuário
        theme_user = ThemeUser.objects.filter(user=user).first()
        theme_data = None
        if theme_user:
            theme_global = theme_user.theme
            theme_serializer = ThemeGlobalSerializer(theme_global)
            theme_data = theme_serializer.data

        log_profile_view(request, slug)

        app_copyright = True if get_user_plan.plan.name == 'GRÁTIS' else False
        form_contact = FormContactEmail.objects.get(user=user).is_activate


        return Response({

            "id": user.id,
            "image": profile.image,
            "banner": profile.banner,
            "name": user.name,
            "full_name": user.full_name,
            "email": user.email,
            "slug": profile.slug,
            "biografy": profile.biografy,
            "links": link_serializer.data,
            "snaps": snap_serializer.data,
            "notes": note_serializer.data, 
            "form_contact": form_contact,
            "copyright": app_copyright,
            "theme": theme_data, 
        })
    
class AuthenticatedUserProfileView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        profile = get_object_or_404(Profile, by=request.user)

        user = User.objects.get(pk=profile.by.pk)

        get_user_plan = Subscription.objects.get(user=user)

        links = Link.objects.filter(created_by=user).all().order_by('-created_at')
        link_serializer = LinkSerializer(instance=links, many=True)

        snaps = Snap.objects.filter(created_by=user).all().order_by('-created_at')
        snap_serializer = SnapSerializer(instance=snaps, many=True)

        notes = Note.objects.filter(user=user).all().order_by('-created_at')
        note_serializer = NoteSerializer(instance=notes, many=True)

        app_copyright = True if get_user_plan.plan.name == 'GRÁTIS' else False
        form_contact = FormContactEmail.objects.get(user=user).is_activate

        return Response({

            "id": user.id,
            "image": profile.image,
            "banner": profile.banner,
            "name": user.name,
            "full_name": user.full_name,
            "email": user.email,
            "slug": profile.slug,
            "biografy": profile.biografy,
            "links": link_serializer.data,
            "snaps": snap_serializer.data,
            "notes": note_serializer.data, 
            "form_contact": form_contact,
            "copyright": app_copyright,

        })
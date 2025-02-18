from django.shortcuts import render, get_object_or_404

from .serializers import SnapSerializer
from .models import Snap

from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import (

    IsAuthenticatedOrReadOnly,
    BasePermission,
    SAFE_METHODS

)

from django.contrib.auth import get_user_model

User = get_user_model()

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.created_by == request.user

class SnapViewSet(ModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    serializer_class = SnapSerializer

    def get_queryset(self):
    
        user = get_object_or_404(User, id=self.request.user.id)

        snaps = Snap.objects.filter(created_by=user).order_by('-created_at')

        return snaps

    def perform_create(self, serializer):

        serializer.save(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):

        owner = get_object_or_404(User, id=request.user.id)

        snap = self.get_object()

        if snap.created_by != owner:

            raise NotFound(detail='Este snap não foi encontrado')

        serializer = self.get_serializer(snap)

        return Response(serializer.data)


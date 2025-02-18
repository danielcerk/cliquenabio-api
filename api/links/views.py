from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    IsAuthenticatedOrReadOnly,
    BasePermission,
    SAFE_METHODS

)

from .serializers import LinkSerializer
from .models import Link

from django.contrib.auth import get_user_model

User = get_user_model()

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.created_by == request.user

class LinkViewSet(ModelViewSet):
    
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    serializer_class = LinkSerializer

    def get_queryset(self):
    
        user = get_object_or_404(User, id=self.request.user.id)

        links = Link.objects.filter(created_by=user).order_by('-created_at')

        return links

    def perform_create(self, serializer):

        serializer.save(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):

        owner = get_object_or_404(User, id=request.user.id)

        link = self.get_object()

        if link.created_by != owner:

            raise NotFound(detail='Este link não foi encontrado')

        serializer = self.get_serializer(link)

        return Response(serializer.data)



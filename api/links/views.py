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

    permission_classes = (IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly)

    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    def get_queryset(self):
        
        user_id = self.kwargs.get('account_pk')

        if not user_id:

            raise NotFound(detail='Nenhum ID de usuário foi informado.')
        
        owner = get_object_or_404(User, pk=user_id)

        links = Link.objects.filter(created_by=owner).order_by('-created_at')

        return links

    def retrieve(self, request, *args, **kwargs):

        user_id = self.kwargs.get('account_pk')

        if not user_id:

            raise NotFound(detail="Nenhum ID de usuário foi informado.")

        owner = get_object_or_404(User, id=user_id)

        link = self.get_object()

        if link.created_by != owner:

            raise NotFound(detail="Este produto não pertence a este usuário.")

        serializer = self.get_serializer(link)

        return Response(serializer.data)


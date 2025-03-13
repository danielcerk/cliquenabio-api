from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    IsAuthenticatedOrReadOnly,
    BasePermission,
    SAFE_METHODS

)

from .serializers import NoteSerializer
from .models import Note

from django.contrib.auth import get_user_model

User = get_user_model()

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.user == request.user

class NoteViewSet(ModelViewSet):
    
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    serializer_class = NoteSerializer

    def get_queryset(self):
    
        user = get_object_or_404(User, id=self.request.user.id)

        notes = Note.objects.filter(user=user).order_by('-created_at')

        return notes

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):

        owner = get_object_or_404(User, id=request.user.id)

        note = self.get_object()

        if note.user != owner:

            raise NotFound(detail='Esta nota não foi encontrada')

        serializer = self.get_serializer(note)

        return Response(serializer.data)



from django.shortcuts import get_object_or_404

from .models import Feedback
from .serializers import FeedbackSerializer

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    BasePermission,
    SAFE_METHODS
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from django.contrib.auth import get_user_model

User = get_user_model()

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.user == request.user

class FeedBackViewSet(ModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    serializer_class = FeedbackSerializer

    def get_queryset(self):

        user = get_object_or_404(User, id=self.request.user.id)

        feedbacks = Feedback.objects.filter(user=user).order_by('-created_at')

        return feedbacks
    
    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
        
    def retrieve(self, request, *args, **kwargs):

        user = get_object_or_404(User, id=request.user.id)

        feedback = self.get_object()

        if feedback.user != user:

            raise NotFound(detail='Este feedback não foi encontrado')

        serializer = self.get_serializer(feedback)

        return Response(serializer.data)
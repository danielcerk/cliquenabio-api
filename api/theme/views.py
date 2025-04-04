from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    BasePermission,
    SAFE_METHODS
)
from .serializers import UserThemeSerializer
from .models import UserTheme
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAdminUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser

class UserThemeViewSet(ModelViewSet):
    """
    ViewSet para administradores gerenciarem todos os temas de usuários
    """
    permission_classes = [IsAdminUser]
    serializer_class = UserThemeSerializer
    queryset = UserTheme.objects.all()
    lookup_field = 'user__id'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserTheme
from .serializers import UserThemeSerializer

class UserThemeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        theme, created = UserTheme.objects.get_or_create(
            user=request.user,
            defaults={
                'background_color': '#ffffff',
                'foreground_color': '#000000',
                'font_family': 'Arial, sans-serif'
            }
        )
        serializer = UserThemeSerializer(theme)
        return Response(serializer.data)

    def put(self, request):
        theme = UserTheme.objects.get(user=request.user)
        serializer = UserThemeSerializer(instance=theme, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

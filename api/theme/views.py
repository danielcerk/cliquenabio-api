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

from .serializers import (
    ThemeGlobalSerializer, ThemeUserSerializer
)
from .models import ThemeGlobal, ThemeUser
from django.contrib.auth import get_user_model

User = get_user_model()

# ThemeUser olny GET and PUT methods

class IsAdminUserOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return request.user.is_superuser

class ThemeGlobalViewSet(ModelViewSet):

    permission_classes = [IsAdminUserOrReadOnly, IsAuthenticatedOrReadOnly]

    serializer_class = ThemeGlobalSerializer
    queryset = ThemeGlobal.objects.all()

class ThemeUserAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        user = get_object_or_404(User, pk=request.user.pk)

        theme_user = get_object_or_404(ThemeUser, user=user)
        serializer = ThemeUserSerializer(theme_user, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        user = get_object_or_404(User, pk=request.user.pk)

        theme_user = get_object_or_404(ThemeUser, user=user)
        serializer = ThemeUserSerializer(instance=theme_user, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .serializers import DashboardSerializer, AdminDashboardSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

class AdminDashboardView(APIView):
    
    permission_classes = (IsAdminUser,)

    def get(self, request):

        serializer = AdminDashboardSerializer({})

        return Response(serializer.data, status=status.HTTP_200_OK)

class DashboardView(APIView):

    def get(self, request):

        user = get_object_or_404(User, id=request.user.id)

        serializer = DashboardSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
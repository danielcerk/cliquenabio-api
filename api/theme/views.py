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
        user = request.user  # Obtém o usuário autenticado
        theme_user = ThemeUser.objects.filter(user=user).first()  # Busca o ThemeUser do usuário

        if not theme_user:
            return Response({"error": "Tema do usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Busca o tema global associado ao ThemeUser
        theme_global = theme_user.theme

        # Serializa o tema global para retornar os detalhes completos
        theme_global_serializer = ThemeGlobalSerializer(theme_global)

        return Response(theme_global_serializer.data, status=status.HTTP_200_OK)



    def put(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.pk)
        theme_user = get_object_or_404(ThemeUser, user=user)

        # Atualiza o ThemeGlobal associado ao ThemeUser
        theme_global = theme_user.theme
        theme_global_serializer = ThemeGlobalSerializer(
            instance=theme_global,
            data=request.data,
            partial=True
        )

        if theme_global_serializer.is_valid():
            theme_global_serializer.save()  # Salva as alterações no ThemeGlobal
            return Response(theme_global_serializer.data, status=status.HTTP_200_OK)
        
        return Response(theme_global_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
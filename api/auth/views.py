from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (

    AllowAny,
    IsAuthenticatedOrReadOnly,
    BasePermission,
    SAFE_METHODS

)
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    AccountSerializer
)

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.views import View

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings

from urllib.parse import urljoin

import requests
from django.urls import reverse

User = get_user_model()

class IsOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.pk == request.user.pk


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Você foi registrado!",
                "user": {
                    "name": user.name,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    "email": user.email,
                },
            },
            status=status.HTTP_201_CREATED,
        )

class AccountViewSet(ViewSet):

    @action(detail=False, methods=['get', 'put', 'delete'], url_path='me')
    def me(self, request):

        user = get_object_or_404(User, id=request.user.id)

        if request.method == 'GET':

            serializer = AccountSerializer(user)
            
            return Response(serializer.data)

        elif request.method == 'PUT':

            serializer = AccountSerializer(user, data=request.data, partial=True)

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        elif request.method == 'DELETE':

            user.delete()

            return Response({"detail": "Usuário deletado com sucesso."})

class GoogleLogin(SocialLoginView):

    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

class GoogleLoginCallback(APIView):

    def get(self, request, *args, **kwargs):

        code = request.GET.get("code")

        if code is None:

            return Response({"error": "Código de autenticação não encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
            "grant_type": "authorization_code",
        }

        response = requests.post(token_url, data=data)

        if response.status_code != 200:

            return Response({"error": "Erro ao obter o token", "content": response.text}, status=status.HTTP_400_BAD_REQUEST)

        token_data = response.json()
        access_token = token_data.get("access_token")

        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(user_info_url, headers=headers)

        if user_info_response.status_code != 200:

            return Response({"error": "Erro ao obter informações do usuário"}, status=status.HTTP_400_BAD_REQUEST)

        user_data = user_info_response.json()

        email = user_data.get("email")
        name = user_data.get("name")

        # Criar ou autenticar o usuário no banco de dados
        user, created = User.objects.get_or_create(email=email, defaults={"name": name})

        # Gerar tokens JWT para autenticação
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "email": user.email,
                "name": user.name,
            }
        })

class LogoutAPIView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):

        try:

            refresh_token = request.data['refresh_token']

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:

            return Response(status=status.HTTP_400_BAD_REQUEST)
    
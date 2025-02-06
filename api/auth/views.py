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
from django.shortcuts import get_object_or_404

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

    '''def list(self, request):

        self.permission_classes = (AllowAny,)

        users = User.objects.all().order_by('-created_at')
        serializer = AccountSerializer(users, many=True)

        return Response(serializer.data)

    def retrieve(self, request):

        self.permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

        user = get_object_or_404(User, id=request.user)

        serializer = AccountSerializer(user, fields=["id", 'name',
            'first_name', 'last_name', 'email', 
            'full_name','biografy', 'image', 'password'])

        return Response(serializer.data)
    

    def update(self, request):

        self.permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

        user = get_object_or_404(User, id=request.user)

        if not user == request.user:

            raise PermissionDenied("Você não tem permissão para editar este perfil.")
            
            
        serializer = AccountSerializer(User, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request):

        self.permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

        user = get_object_or_404(User, id=request.user)

        if user != request.user:

            raise PermissionDenied("Você não tem permissão para deletar este perfil.")
            
        user.delete()

        return Response({"detail": "Usuário deletado com sucesso."})'''


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
    
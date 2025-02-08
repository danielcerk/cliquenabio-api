from django.shortcuts import get_object_or_404

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    BasePermission,
    SAFE_METHODS
)

from .serializers import ContactEmailSerializer, FormContactEmailSerializer
from .models import FormContactEmail

from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .utils import send_email_for_user

User = get_user_model()

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.user == request.user

class FormContactEmailAPIView(APIView):

    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request, *args, **kwargs):

        user = get_object_or_404(
            User, pk=request.user.id
        )

        get_form_contact_email = get_object_or_404(
            FormContactEmail, user=user
        )

        serializer = FormContactEmailSerializer(instance=get_form_contact_email)

        return Response(serializer.data)


    def put(self, request, *args, **kwargs):

        user = get_object_or_404(
            User, pk=request.user.id
        )

        get_form_contact_email = get_object_or_404(
            FormContactEmail, user=user
        )

        serializer = FormContactEmailSerializer(
            instance=get_form_contact_email, 
            data=request.data, 
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class ContactEmailAPIView(APIView):

    permission_classes = [AllowAny,]

    def post(self, request, id, *args, **kwargs):

        id = self.kwargs.get('id')

        recipient = get_object_or_404(User, pk=id)

        serializer = ContactEmailSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data['email']
            content = serializer.validated_data['content']

            send_email_for_user(email, content, recipient.email)

            return Response({'message': 'Email enviado com sucesso!'}, status=200)
        
        return Response(serializer.errors, status=400)
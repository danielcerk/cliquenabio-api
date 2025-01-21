from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import FormContactEmailSerializer

from django.contrib.auth import get_user_model
from django.core.mail import send_mail

message = '''


%s te enviou um email com o seguinte conteúdo:

%s


'''

User = get_user_model()

class FormContactAPIView(APIView):

    permission_classes = [AllowAny,]

    def post(self, request, id, *args, **kwargs):

        recipient = User.objects.get(pk=id)

        serializer = FormContactEmailSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data['email']
            content = serializer.validated_data['content']

            greeting_message = message % (email, content)

            send_mail(
                'Alguém te mandou uma mensagem no CliqueNaBio!',
                greeting_message,
                'suporteconstsoft@gmail.com',
                [recipient.email],
                fail_silently=False,
            )

            return Response({'message': 'Email enviado com sucesso!'}, status=200)
        
        return Response(serializer.errors, status=400)
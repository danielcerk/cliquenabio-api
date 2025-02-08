from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .models import ContactEmail

message = '''


%s te enviou um email com o seguinte conteúdo:

" %s "


'''

User = get_user_model()

def send_email_for_user(sender_email, 
    content, recipient_email):

    greeting_message = message % (sender_email, content)

    user = get_object_or_404(User, email=recipient_email)

    form_contact = ContactEmail.objects.create(
        user=user, 
        sender_email=sender_email, content=content
    )

    form_contact.save()

    send_mail(
        'Alguém te mandou uma mensagem no CliqueNaBio!',
        greeting_message,
        'suporteconstsoft@gmail.com',
        [recipient_email],
        fail_silently=False,
    )
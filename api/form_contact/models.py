from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Layout for contact, each user has one
class FormContactEmail(models.Model):

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, verbose_name='Usuário'
    )

    is_activate = models.BooleanField(
        default=True, verbose_name='Está ativado')

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Atualizado em'
    )

    class Meta:

        verbose_name = 'Layout de Email'
        verbose_name_plural = 'Layouts de Emails'

    def __str__(self):

        return f'Layout de email de {self.user}'

class ContactEmail(models.Model):

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, verbose_name='Usuário'
    )

    sender_email = models.EmailField(verbose_name='Remetente')
    content = models.TextField(verbose_name='Conteúdo')


    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Atualizado em'
    )

    class Meta:

        verbose_name = 'Email enviado'
        verbose_name_plural = 'Emails enviados'

    def __str__(self):

        return '%s enviou um email para %s' % (self.sender_email, self.user.email)
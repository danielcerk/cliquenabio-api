from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

from .models import UserProfile

message = '''

Ei %s,

Bem-vindo ao CliqueNaBio! 🚀

Estamos empolgados em tê-lo conosco! O CliqueNaBio oferece uma solução completa para transformar o seu link na bio em uma verdadeira vitrine digital. Com nossa plataforma intuitiva e totalmente personalizável, você pode facilmente criar um espaço único para compartilhar momentos especiais, trabalhos, links importantes e muito mais, tudo em um só lugar.

O que você pode fazer com o CliqueNaBio:

- Personalizar sua página: Escolha o layout, cores e conteúdo de forma simples e elegante.
- Adicionar links dinâmicos: Insira links para suas redes sociais, portfólio, loja online e qualquer outro conteúdo relevante.
- Mostrar seus trabalhos: Crie uma galeria para destacar seus projetos, artigos ou qualquer conteúdo visual que deseje compartilhar.
- Exibir momentos: Mostre os melhores momentos da sua jornada, criando um espaço envolvente e personalizado.
- E muito mais: Funcionalidades extras para tornar sua página ainda mais interessante e única!

Pronto para começar a personalizar seu link na bio? Explore agora e crie algo incrível!

'''

@receiver(post_save, sender=UserProfile)
def create_user_profile(sender, instance, created, **kwargs):

	if created:

		# Send Email to user
		
		greeting_message = message % instance.name

		send_mail(
			'Bem-Vindo ao CliqueNaBio e venha deixar seu link na bio a sua cara!',
			greeting_message,
			'suporteconstsoft@gmail.com',
			[instance.email],
			fail_silently=False,

		)
		
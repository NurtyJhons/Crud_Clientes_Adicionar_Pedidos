from django.core.signing import TimestampSigner
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

signer = TimestampSigner()

def gerar_link_confirmacao_email(cliente):
    token = signer.sign(str(cliente.pk))  # Certifique-se que é string
    url = reverse('confirmar_email', args=[token])
    return f"http://localhost:8000{url}"

def enviar_email_boas_vindas(cliente):
    assunto = "Bem-vindo ao nosso sistema!"
    mensagem = f"Olá {cliente.nome},\n\nSeu e-mail foi confirmado com sucesso. Seja bem-vindo!"
    remetente = settings.DEFAULT_FROM_EMAIL
    destinatario = [cliente.email]

    send_mail(
        assunto,
        mensagem,
        remetente,
        destinatario,
        fail_silently=False,
    )

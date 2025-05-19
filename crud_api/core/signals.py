from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import Cliente

@receiver(post_save, sender=User)
def criar_cliente_automaticamente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(usuario=instance, nome=instance.username, email=instance.email)


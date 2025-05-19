from django.contrib.auth.models import User, AbstractUser  # Adicione isso no topo
from django.db import models

# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    criado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class ClienteFinal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ← troque aqui
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)  # será armazenada com hash
    telefone = models.CharField(max_length=20, blank=True) 
    criado_em = models.DateTimeField(auto_now_add=True)
    email_confirmado = models.BooleanField(default=False)
    imagem_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)

    def __str__(self):
        return self.nome
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status, serializers
from .serializers import ProdutoSerializer, ItemCarrinhoSerializer, CarrinhoSerializer
from .models import Produto, ItemCarrinho, Carrinho
from core.models import ClienteFinal
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class CarrinhoViewSet(ModelViewSet):
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Carrinho.objects.filter(cliente=self.request.user)

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.cliente != self.request.user:
            raise PermissionDenied("Você não pode editar carrinhos de outros usuários.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.cliente != self.request.user:
            raise PermissionDenied("Você não pode remover carrinhos de outros usuários.")
        instance.delete()

class ItemCarrinhoViewSet(ModelViewSet):
    queryset = ItemCarrinho.objects.all()
    serializer_class = ItemCarrinhoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemCarrinho.objects.filter(carrinho__cliente=self.request.user)

    def perform_create(self, serializer):
        carrinho = serializer.validated_data.get('carrinho')
        if carrinho.cliente != self.request.user:
            raise PermissionDenied("Você não pode adicionar itens em carrinhos de outros usuários.")
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.carrinho.cliente != self.request.user:
            raise PermissionDenied("Você não pode editar itens de carrinhos de outros usuários.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.carrinho.cliente != self.request.user:
            raise PermissionDenied("Você não pode remover itens de carrinhos de outros usuários.")
        instance.delete()
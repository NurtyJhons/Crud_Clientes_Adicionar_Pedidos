from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status, serializers
from .serializers import ProdutoSerializer, ItemCarrinhoSerializer, CarrinhoSerializer
from .models import Produto, ItemCarrinho, Carrinho
from core.models import ClienteFinal
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class CarrinhoViewSet(viewsets.ModelViewSet):
    serializer_class = CarrinhoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Carrinho.objects.filter(cliente=self.request.user.ClienteFinal)

    def create(self, request, *args, **kwargs):
        carrinho_existente = Carrinho.objects.filter(cliente=request.user.ClienteFinal, status='aberto').first()
        if carrinho_existente:
            serializer = self.get_serializer(carrinho_existente)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cliente=request.user.ClienteFinal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from rest_framework.exceptions import PermissionDenied

class ItemCarrinhoViewSet(viewsets.ModelViewSet):
    serializer_class = ItemCarrinhoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemCarrinho.objects.filter(carrinho__cliente=self.request.user.ClienteFinal)

    def perform_create(self, serializer):
        carrinho = Carrinho.objects.filter(cliente=self.request.user.ClienteFinal, status='aberto').first()
        if not carrinho:
            raise serializers.ValidationError("Nenhum carrinho aberto encontrado para este usuário.")
        serializer.save(carrinho=carrinho)


    def perform_update(self, serializer):
        carrinho = serializer.instance.carrinho
        if carrinho.cliente != self.request.user.ClienteFinal:
            raise PermissionDenied("Você não pode editar itens de carrinhos de outros usuários.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.carrinho.cliente != self.request.user.ClienteFinal:
            raise PermissionDenied("Você não pode excluir itens de carrinhos de outros usuários.")
        instance.delete()
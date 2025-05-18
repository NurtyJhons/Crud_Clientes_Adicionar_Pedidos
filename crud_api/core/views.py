from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Cliente
from .serializers import ClienteSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email']
    ordering_fields = ['nome', 'criado_em']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


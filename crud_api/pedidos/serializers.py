from rest_framework import serializers
from .models import Produto, Carrinho, ItemCarrinho

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class ItemCarrinhoSerializer(serializers.ModelSerializer):
    nome_produto = serializers.ReadOnlyField(source='produto.nome')
    preco_produto = serializers.ReadOnlyField(source='produto.preco')
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarrinho
        fields = ['id', 'produto', 'nome_produto', 'preco_produto', 'quantidade', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()

class CarrinhoSerializer(serializers.ModelSerializer):
    itens = ItemCarrinhoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Carrinho
        fields = ['id', 'cliente', 'criado_em', 'itens', 'total']
        read_only_fields = ['cliente', 'criado_em']

    def get_total(self, obj):
        return sum(item.subtotal() for item in obj.itens.all())


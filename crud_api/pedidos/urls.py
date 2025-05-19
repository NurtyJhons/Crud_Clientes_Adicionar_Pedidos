from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProdutoViewSet, CarrinhoViewSet, ItemCarrinhoViewSet

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'carrinhos', CarrinhoViewSet, basename='carrinho')
router.register(r'itens-carrinho', ItemCarrinhoViewSet, basename='itemcarrinho')

urlpatterns = [
    path('', include(router.urls)),
]
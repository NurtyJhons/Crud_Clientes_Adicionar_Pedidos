from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import ClienteViewSet
from . import views_cliente
from .views_cliente import index, confirmar_email
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)

urlpatterns = [
    # Rotas da API
    path('', include(router.urls)),
    path('auth/', obtain_auth_token),

    # Páginas HTML dos clientes
    path('registro/', views_cliente.registro_cliente, name='registro_cliente'),
    path('', index, name='pagina_inicial'),
    path('login/', views_cliente.login_cliente, name='login_cliente'),
    path('painel/', views_cliente.painel_cliente, name='painel_cliente'),
    path('logout/', views_cliente.logout_cliente, name='logout_cliente'),
    path('editar/', views_cliente.editar_cliente, name='editar_cliente'), 
    path('trocar-senha/', views_cliente.trocar_senha, name='trocar_senha'),
    path('excluir-conta/', views_cliente.excluir_conta, name='excluir_conta'),
    path('clientes/confirmar-email/<str:token>/', views_cliente.confirmar_email, name='confirmar_email'),

    # Rotas de redefinição de senha
    path('senha-esquecida/', auth_views.PasswordResetView.as_view(
        template_name='clientes/senha_esquecida.html'
    ), name='password_reset'),
    path('senha-enviada/', auth_views.PasswordResetDoneView.as_view(
        template_name='clientes/senha_enviada.html'
    ), name='password_reset_done'),
    path('redefinir-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='clientes/redefinir_senha.html'
    ), name='password_reset_confirm'),
    path('senha-concluida/', auth_views.PasswordResetCompleteView.as_view(
        template_name='clientes/senha_concluida.html'
    ), name='password_reset_complete'),
]
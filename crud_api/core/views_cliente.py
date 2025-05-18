from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import ClienteFinal
from .forms import RegistroClienteForm, LoginClienteForm, ClienteFinalUpdateForm, TrocaSenhaForm
from django.contrib.auth.decorators import login_required
from core.utils import gerar_link_confirmacao_email, signer
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.core.signing import BadSignature, SignatureExpired
from core.models import Cliente
from core.utils import enviar_email_boas_vindas

def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.senha = make_password(form.cleaned_data['senha'])
            cliente.save()  # SALVAR PRIMEIRO para gerar o ID

            # AGORA o cliente.pk existe, então podemos gerar o link
            link = gerar_link_confirmacao_email(cliente)

            send_mail(
                'Confirmação de e-mail',
                f'Clique no link para confirmar seu e-mail: {link}',
                settings.DEFAULT_FROM_EMAIL,
                [cliente.email],
            )

            messages.success(request, 'Cadastro realizado com sucesso! Verifique seu e-mail para confirmar.')
            return redirect('login_cliente')
    else:
        form = RegistroClienteForm()
    return render(request, 'clientes/registro.html', {'form': form})

def login_cliente(request):
    if request.method == 'POST':
        form = LoginClienteForm(request.POST)
        if form.is_valid():
            try:
                cliente = ClienteFinal.objects.get(email=form.cleaned_data['email'])
                if check_password(form.cleaned_data['senha'], cliente.senha):
                    request.session['cliente_id'] = cliente.id
                    return redirect('painel_cliente')
                else:
                    messages.error(request, 'Senha incorreta.')
            except ClienteFinal.DoesNotExist:
                messages.error(request, 'E-mail não encontrado.')
    else:
        form = LoginClienteForm()
    return render(request, 'clientes/login.html', {'form': form})

def painel_cliente(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login_cliente')
    
    cliente = ClienteFinal.objects.get(id=cliente_id)
    return render(request, 'clientes/painel.html', {'cliente': cliente})

def logout_cliente(request):
    request.session.flush()
    return redirect('login_cliente')

def editar_cliente(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login_cliente')

    cliente = ClienteFinal.objects.get(id=cliente_id)

    if request.method == 'POST':
        form = ClienteFinalUpdateForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('painel_cliente')
    else:
        form = ClienteFinalUpdateForm(instance=cliente)

    return render(request, 'clientes/editar_perfil.html', {'form': form})

def trocar_senha(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login_cliente')

    cliente = ClienteFinal.objects.get(id=cliente_id)

    if request.method == 'POST':
        form = TrocaSenhaForm(request.POST)
        if form.is_valid():
            if not check_password(form.cleaned_data['senha_atual'], cliente.senha):
                form.add_error('senha_atual', 'Senha atual incorreta.')
            elif form.cleaned_data['nova_senha'] != form.cleaned_data['confirmar_nova_senha']:
                form.add_error('confirmar_nova_senha', 'As senhas não coincidem.')
            else:
                cliente.senha = make_password(form.cleaned_data['nova_senha'])
                cliente.save()
                messages.success(request, 'Senha atualizada com sucesso!')
                return redirect('painel_cliente')
    else:
        form = TrocaSenhaForm()

    return render(request, 'clientes/trocar_senha.html', {'form': form})

def excluir_conta(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login_cliente')

    cliente = ClienteFinal.objects.get(id=cliente_id)

    if request.method == 'POST':
        cliente.delete()
        request.session.flush()
        messages.success(request, 'Sua conta foi excluída com sucesso.')
        return redirect('registro_cliente')

    return render(request, 'clientes/excluir_conta.html')

def index(request):
    return render(request, 'clientes/index.html')

def confirmar_email(request, token):
    try:
        cliente_id = int(signer.unsign(token, max_age=60*60*24))
        cliente = ClienteFinal.objects.get(pk=cliente_id)  # Alterado de Cliente para ClienteFinal
        cliente.email_confirmado = True
        cliente.save()
        enviar_email_boas_vindas(cliente)

        return HttpResponse("E-mail confirmado com sucesso!")
    except (BadSignature, SignatureExpired, ClienteFinal.DoesNotExist, ValueError):
        return HttpResponse("Link inválido ou expirado.")

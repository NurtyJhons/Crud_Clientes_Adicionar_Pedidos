from django import forms
from .models import ClienteFinal

class RegistroClienteForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ClienteFinal
        fields = ['nome', 'email', 'senha']

class LoginClienteForm(forms.Form):
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)

class ClienteFinalUpdateForm(forms.ModelForm):
    class Meta:
        model = ClienteFinal
        fields = ['nome', 'email', 'telefone', 'imagem_perfil']

class TrocaSenhaForm(forms.Form):
    senha_atual = forms.CharField(widget=forms.PasswordInput, label="Senha atual")
    nova_senha = forms.CharField(widget=forms.PasswordInput, label="Nova senha")
    confirmar_nova_senha = forms.CharField(widget=forms.PasswordInput, label="Confirmar nova senha")

class RegistroClienteForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ClienteFinal
        fields = ['nome', 'email', 'telefone', 'senha']

    def clean_email(self):
        email = self.cleaned_data['email']
        if ClienteFinal.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email
    
    def clean_senha(self):
        senha = self.cleaned_data['senha']
        if len(senha) < 8:
            raise forms.ValidationError("A senha deve ter no mínimo 8 caracteres.")
        return senha


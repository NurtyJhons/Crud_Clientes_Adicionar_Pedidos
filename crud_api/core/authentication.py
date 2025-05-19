from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from core.models import ClienteFinal

class ClienteFinalTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Token inválido.')

        try:
            cliente_final = ClienteFinal.objects.get(user=token.user)
        except ClienteFinal.DoesNotExist:
            raise AuthenticationFailed('Usuário não encontrado.')

        return (cliente_final, token)

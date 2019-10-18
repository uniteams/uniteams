from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication

from authapp.models import UniteamsUser
from api_v1.exceptions import UniteamsAPIException
from api_v1.authapp import errorcodes

UserModel = get_user_model()


class JWTAuthentication(authentication.TokenAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        if len(auth_header) > 2:
            return None
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(token)

    @staticmethod
    def _authenticate_credentials(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.InvalidTokenError:
            raise UniteamsAPIException(**errorcodes.ERR_INVALID_TOKEN)

        dt_exp = datetime.fromtimestamp(int(payload['exp']))
        if dt_exp < datetime.now():
            raise UniteamsAPIException(**errorcodes.ERR_TOKEN_OUT_OF_DATE)
        try:
            user = UniteamsUser.objects.get(pk=payload['user_id'])
        except UniteamsUser.DoesNotExist:
            raise UniteamsAPIException(**errorcodes.ERR_TOKEN_NOT_SEARCH_USER)

        if not user.is_active:
            raise UniteamsAPIException(**errorcodes.ERR_TOKEN_NOT_SEARCH_USER)
        return user, token
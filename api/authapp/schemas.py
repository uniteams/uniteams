import coreapi
import coreschema
from rest_framework.schemas import AutoSchema


class UniteamsUsersSchema(AutoSchema):
    def get_description(self, path, method):

        if path == '/auth/signup/':
            return 'Создание нового пользователя.'
        if path == '/api/auth/signin/':
            return 'Авторизация по логину и паролю.'

        return None

    def get_encoding(self, path, method):
        return 'application/json'

    def get_serializer_fields(self, path, method):
        fields = []
        if method == 'POST':
            fields = [
                coreapi.Field(
                    "login",
                    required=True,
                    location="form",
                    schema=coreschema.String(title="Username",
                                             description="Valid username for authentication"),
                    description='username'
                ),
                coreapi.Field(
                    "password",
                    required=True,
                    location="form",
                    schema=coreschema.String(),
                    description='Password',
                ),
            ]
        return fields
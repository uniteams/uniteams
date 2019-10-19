from django.contrib.auth import authenticate
from rest_framework import serializers

from api_v1.authapp import errorcodes
from api_v1.exceptions import UniteamsAPIException
from authapp.models import UniteamsUser


class UniteamsUsersSerializer(serializers.ModelSerializer):
    # token = serializers.CharField(max_length=512, write_only=True)
    #
    # def validate_token(self, value):
    #     model_class = self.Meta.model
    #     user = model_class.objects.filter(token=value)
    #     print(user)
    #     if not model_class.objects.filter(token=value).exists():
    #         raise UniteamsAPIException(**errorcodes.ERR_TOKEN_NOT_SEARCH_USER)
    #     if len(value) < 3 or len(value) > 512:
    #         print(len(value), value)
    #         raise UniteamsAPIException(**errorcodes.ERR_WRONG_TOKEN)
    #     return value

    class Meta:
        model = UniteamsUser
        fields = ['token']


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)

    # token = serializers.CharField(max_length=255, read_only=True)

    def validate_username(self, value):
        model_class = self.Meta.model
        if model_class.objects.filter(username=value).exists():
            raise UniteamsAPIException(**errorcodes.ERR_LOGIN_ALREADY_EXIST)
        if len(value) < 3 or len(value) > 19:
            raise UniteamsAPIException(**errorcodes.ERR_WRONG_LOGIN)
        return value

    @staticmethod
    def validate_password(value):
        # TODO Provide to checking a password
        # if len(value) != 64:
        #     raise UniteamsAPIException(**errorcodes.ERR_WRONG_PASSWORD)
        return value

    class Meta:
        model = UniteamsUser

        fields = ['username', 'email', 'password']

    def create(self, validated_data):

        user = UniteamsUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise UniteamsAPIException(**errorcodes.ERR_WRONG_LOGIN)
        if password is None:
            raise UniteamsAPIException(**errorcodes.ERR_WRONG_PASSWORD)

        user = authenticate(username=username, password=password)

        if user is None:
            raise UniteamsAPIException(**errorcodes.ERR_WRONG_LOGIN_OR_PASSWRD)

        return {
            'access_token': user.token,
            "token_type": "Bearer",
        }

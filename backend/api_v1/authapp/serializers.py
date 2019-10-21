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
        user.generate_activation_key()
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


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    activation_key = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', '')
        activation_key = data.get('activation_key', '')

        if email is None or activation_key is None:
            raise UniteamsAPIException(**errorcodes.ERR_WRONG_ACTIVATION_KEY)

        user = UniteamsUser.objects.get(email=email, activation_key=activation_key)
        if user is None:
            raise UniteamsAPIException(**errorcodes.ERR_USER_NOT_FOUND)
        if user.is_active:
            raise UniteamsAPIException(**errorcodes.ERR_USER_ALREADY_ACTIVATED)
        if user.is_activation_key_expired:
            raise UniteamsAPIException(**errorcodes.ERR_ACTIVATION_KEY_EXPIRED)
        return {
            'email': user.email,
            'activation_key': user.activation_key
        }

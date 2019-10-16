from rest_framework import serializers

from django.contrib.auth import authenticate

from authapp import errorcodes
from authapp.exceptions import UniteamsAuthException

from authapp.models import UniteamsUser, Company



class UniteamsUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UniteamsUser
        fields = ['url', 'username', 'email', 'groups']


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate_username(self, value):
        model_class = self.Meta.model
        if model_class.objects.filter(username=value).exists():
            raise UniteamsAuthException(**errorcodes.ERR_LOGIN_ALREADY_EXIST)
        if len(value) < 3 or len(value) > 19:
            raise UniteamsAuthException(**errorcodes.ERR_WRONG_LOGIN)
        return value

    @staticmethod
    def validate_password(value):
        if len(value) != 64:
            raise UniteamsAuthException(**errorcodes.ERR_WRONG_PASSWORD)
        return value

    class Meta:
        model = UniteamsUser

        fields = ['username', 'email', 'password', 'token']

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
            raise UniteamsAuthException(**errorcodes.ERR_WRONG_LOGIN)
        if password is None:
            raise UniteamsAuthException(**errorcodes.ERR_WRONG_PASSWORD)

        user = authenticate(username=username, password=password)

        if user is None:
            raise UniteamsAuthException(**errorcodes.ERR_WRONG_LOGIN_OR_PASSWRD)

        return {
            'token': user.token
        }

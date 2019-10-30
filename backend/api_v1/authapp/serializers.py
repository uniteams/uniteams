from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, mixins
from rest_framework.reverse import reverse

from api_v1.authapp import errorcodes
from api_v1.exceptions import UniteamsAPIException
from authapp.models import UserProfile, Company

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)

    links = serializers.SerializerMethodField('get_links')
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        error_messages={'does_not_exist': 'Invalid category id'}, )

    class Meta:
        model = User
        fields = ['user', 'id', 'email', 'username', 'links']
        read_only_fields = ['user', 'id', 'email', 'username']

    def get_links(self, obj):
        request = self.context['request']
        print(self.context['users'])
        pk = obj.get('id')
        return {

            # 'self': reverse('api-v1:auth:user-detail', kwargs={'pk': pk}, request=request)
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.generate_activation_key()
        return user


class UserListSerializer(serializers.ListSerializer):
    child = UserSerializer()

    def validate_child(self, value):
        print(value)
        return value

    def validate(self, attrs):
        return attrs


class UserProfileSerializer(mixins.UpdateModelMixin, serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    middle_name = serializers.CharField(read_only=True)
    gender = serializers.CharField(read_only=True)
    position = serializers.CharField(read_only=True)
    links = serializers.SerializerMethodField('get_links')

    class Meta:
        model = UserProfile
        fields = ['user_id', 'first_name', 'last_name', 'middle_name', 'gender', 'position', 'links']

    def get_links(self, obj):
        request = self.context['request']
        pk = self.context.get('pk')
        return {
            'self': reverse('api-v1:auth:user-detail', kwargs={'pk': pk}, request=request),
            'users': reverse('api-v1:auth:users', request=request)
        }

    def validate(self, data):
        pk = self.context.get('pk')
        user_profile = UserProfile.objects.get(user__id=pk)
        return user_profile


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.generate_activation_key()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'links']

    # def validate(self, data):
    #     return data

    def validate(self, data):
        user = User.objects.get(pk=data.get('pk'))
        user_profile = user.get_user_profile()
        return {'first_name': user_profile.first_name}

    def get_links(self, obj):
        request = self.context['request']
        pk = obj.get('pk')
        return {
            'self': reverse('api-v1:auth:user-detail', kwargs={'pk': pk}, request=request),
            'users': reverse('api-v1:auth:users', request=request)
        }


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
        model = User

        fields = ['username', 'email', 'password']

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        user.generate_activation_key()
        return user


class TokenSerializer(serializers.Serializer):
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

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise UniteamsAPIException(**errorcodes.ERR_WRONG_LOGIN_OR_PASSWRD)
        else:
            if not user.is_active:
                raise UniteamsAPIException(**errorcodes.ERR_USER_IS_NOT_ACTIVE)

        user = authenticate(username=username, password=password)
        print(user.is_authenticated)
        if user is None:
            raise UniteamsAPIException(**errorcodes.ERR_WRONG_LOGIN_OR_PASSWRD)
        return {
            'token': user.token,
            "token_type": "Bearer",
            'user': user,
        }


class VerifySerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    activation_key = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', '')
        activation_key = data.get('activation_key', '')

        if email is None or activation_key is None:
            raise UniteamsAPIException(**errorcodes.ERR_WRONG_ACTIVATION_KEY)
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise UniteamsAPIException(**errorcodes.ERR_USER_NOT_FOUND)
        else:
            if user.is_active:
                raise UniteamsAPIException(**errorcodes.ERR_USER_ALREADY_ACTIVATED)
            if user.activation_key != activation_key:
                raise UniteamsAPIException(**errorcodes.ERR_WRONG_ACTIVATION_KEY)
            if user.is_activation_key_expired:
                raise UniteamsAPIException(**errorcodes.ERR_ACTIVATION_KEY_EXPIRED)
        return True


class CompanySerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    company_name = serializers.CharField(read_only=True)
    owner = serializers.CharField(read_only=True)
    administrator = serializers.CharField(read_only=True)
    org_struct = serializers.CharField(read_only=True)
    # employees = serializers.CharField(read_only=True)
    links = serializers.SerializerMethodField('get_links')

    class Meta:
        model = Company
        fields = ['pk', 'company_name', 'owner', 'administrator', 'org_struct', 'links']

    def get_links(self, obj):
        request = self.context['request']
        pk = self.context.get('pk')
        return {
            'self': reverse('api-v1:auth:company-detail', kwargs={'pk': pk}, request=request),
            'companies': reverse('api-v1:auth:companies', request=request)
        }

    def validate(self, data):
        pk = self.context.get('pk')
        company = Company.objects.get(pk=pk)
        return company


class CompanyRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        company_name = validated_data.get('company_name')
        company = user.create_company(company_name=company_name)
        return company
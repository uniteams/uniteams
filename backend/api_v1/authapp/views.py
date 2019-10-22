from django.core.mail import EmailMessage
from django.urls import reverse

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import UniteamsUser
from api_v1.authapp.renderers import (RegistrationJSONRenderer, UserJSONRenderer, )
from api_v1.authapp.serializers import (RegistrationSerializer, LoginSerializer, UniteamsUsersSerializer,
                                        VerifySerializer)

from api_v1.authapp.backends import JWTAuthentication
from uniteams import settings


class ListUsersAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UniteamsUsersSerializer

    def get(self, request):
        username = request.data.get('username', '')
        token = request.data.get('token', '')
        user = {'username': username, 'token': token}
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            usernames = [
                {'id': user.id, 'username': user.username, 'email': user.email} for user in UniteamsUser.objects.all()
            ]
            return Response(usernames, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (RegistrationJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        username = request.data.get('username', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        user = {'username': username, 'email': email, 'password': password}
        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = UniteamsUser.objects.get(username=username)
            send_status = user.receive_activation_key()

            if send_status:
                message = f'Registration complete. Activate your account to use it. ' \
                    f'Email with an activation key was successful sent to {user.email}'
            else:
                message = f'Registration complete. But activation key was not send.'

            return Response({'message': message}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = {'username': username, 'password': password}
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = VerifySerializer

    def get(self, request):
        data = request.GET
        email = data.get('email', '')
        activation_key = data.get('activation_key', '')
        user = {'email': email, 'activation_key': activation_key}
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            user = UniteamsUser.objects.get(**user)
            user.activate()
            if user.is_active:
                message = f'User {user.username} was successful activated!'
            else:
                message = f'User {user.username} activation failed'
            return Response({'message': message}, status=status.HTTP_200_OK)


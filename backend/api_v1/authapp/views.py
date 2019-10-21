from django.core.mail import EmailMessage

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
            print(username)

            user = UniteamsUser.objects.get(username=username)

            print(user.activation_key)
            # verify_link = f'{reverse("auth:verify")}?email={user.email}&activation_key={user.activation_key}'
            # email = EmailMessage(settings.EMAIL_ACTIVATION_KEY_SUBJECT,
            #                      f'')
            return Response(serializer.data, status=status.HTTP_200_OK)


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
    renderer_classes = (UserJSONRenderer,)
    serializer_class = VerifySerializer

    def get(self, request):
        email = request.data.get('email', '')
        activation_key = request.data.get('activation_key', '')
        user = {'email': email, 'activation_key': activation_key}
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            user = UniteamsUser(serializer.data)
            user.activate()
            return Response(serializer.data, status=status.HTTP_200_OK)

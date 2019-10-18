import json

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import UniteamsUser
from api_v1.authapp.renderers import (RegistrationJSONRenderer, UserJSONRenderer, )
from api_v1.authapp.serializers import (RegistrationSerializer, LoginSerializer, UniteamsUsersSerializer)

from api_v1.authapp.backends import JWTAuthentication

class ListUsersAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = UniteamsUsersSerializer

    def get(self, request):
        print(request.META)
        username = request.data.get('username', '')
        token = request.data.get('token', '')

        # authentication = self.authentication_classes()
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

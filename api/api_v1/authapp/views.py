import json
from rest_framework import status, viewsets, authentication, permissions
from rest_framework.response import Response
# from rest_framework.schemas.openapi import SchemaGenerator
from rest_framework.views import APIView

from authapp.models import UniteamsUser
from api_v1.authapp.renderers import (RegistrationJSONRenderer, UserJSONRenderer, )
from api_v1.authapp.serializers import (RegistrationSerializer, LoginSerializer, UniteamsUsersSerializer)


# from api_v1.schemas import UniteamsUsersSchema


class ListUsersAPIView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # generator = SchemaGenerator(title='Stock Prices API')
    # schema = generator.get_schema()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """
        Return a list of all users.
        """

        usernames = [user.username for user in UniteamsUser.objects.all()]
        return Response(usernames, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    # schema = UniteamsUsersSchema()
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
    # schema = UniteamsUsersSchema()
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        login = request.data.get('login', '')
        password = request.data.get('password', '')
        user = {'username': login, 'password': password}
        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import UniteamsUser
from api_v1.authapp.renderers import (RegistrationJSONRenderer, UserJSONRenderer, )
from api_v1.authapp.serializers import (RegistrationSerializer, LoginSerializer, UniteamsUserSerializer)

from api_v1.schemas import UniteamsUsersSchema


class UserViewSet(viewsets.ModelViewSet):
    queryset = UniteamsUser.objects.all().order_by('-date_joined')
    serializer_class = UniteamsUserSerializer


class RegistrationAPIView(APIView):
    schema = UniteamsUsersSchema()
    permission_classes = (AllowAny,)
    renderer_classes = (RegistrationJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        login = request.data.get('login', '')
        password = request.data.get('password', '')
        user = {'username': login, 'password': password}

        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    schema = UniteamsUsersSchema()
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        login = request.data.get('login', '')
        password = request.data.get('password', '')
        user = {'username': login, 'password': password}
        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

from django.contrib.auth import get_user_model
from rest_framework import status, mixins
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authapp.models import UniteamsUser, UserProfile
from api_v1.authapp.renderers import UserJSONRenderer
from api_v1.authapp.serializers import RegistrationSerializer, TokenSerializer, UserSerializer, VerifySerializer, \
    UserDetailSerializer, UserRegisterSerializer, UserListSerializer, UserProfileSerializer
from api_v1.authapp.backends import JWTAuthentication

User = get_user_model()


class UsersAPIView(APIView):
    queryset = User.objects.order_by(User.USERNAME_FIELD)

    @permission_classes((IsAdminUser,))
    @authentication_classes((JWTAuthentication,))
    def get(self, request):
        users = [{'id': user.id, 'username': user.username, 'email': user.email} for user in self.queryset.all()]
        serializer = UserListSerializer(data=users, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes((AllowAny,))
    def post(self, request):
        username = request.data.get('username', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = {'username': username, 'email': email, 'password': password}
        serializer = UserRegisterSerializer(data=user)

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


class UserDetailAPIView(UpdateAPIView):
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer
    lookup_field = 'user__id'

    @authentication_classes((JWTAuthentication,))
    @permission_classes((IsAuthenticated,))
    def get(self, request, pk):
        data = {'pk': pk}
        serializer = UserProfileSerializer(data=data,
                                           context={'request': request, 'pk': pk})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

    @authentication_classes((JWTAuthentication,))
    @permission_classes((IsAuthenticated,))
    def put(self, request, *args, **kwargs):
        self.kwargs.update({'user__id': self.kwargs.get('pk')})
        return self.update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        print(request.data)
        instance = self.get_object()
        instance.first_name = request.data.get('first_name', '')
        instance.last_name = request.data.get('last_name', '')
        instance.middle_name = request.data.get('middle_name', '')
        instance.gender = request.data.get('gender', '')
        instance.position = request.data.get('position', '')
        instance.save()
        serializer = self.serializer_class(instance,
                                           data=request.data,
                                           context={'request': request, 'pk': self.kwargs.get('pk')})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
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


class TokenAPIView(APIView):
    renderer_classes = (UserJSONRenderer,)
    serializer_class = TokenSerializer

    @permission_classes((AllowAny,))
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = {'username': username, 'password': password}
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyAPIView(APIView):
    serializer_class = VerifySerializer

    @permission_classes((AllowAny,))
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

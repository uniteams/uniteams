from django.contrib.auth import get_user_model
from rest_framework import status, mixins
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from api_v1.permissions import IsAuthenticatedOnlySelf
from authapp.models import UniteamsUser, UserProfile, Company
from api_v1.authapp.renderers import UserJSONRenderer
from api_v1.authapp.serializers import (RegistrationSerializer, TokenSerializer, UserSerializer, VerifySerializer,
                                        UserDetailSerializer, UserRegisterSerializer, UserProfileSerializer,
                                        UserListSerializer, CompanySerializer)
from api_v1.authapp.backends import JWTAuthentication

User = get_user_model()


class UsersAPIView(APIView):
    queryset = User.objects.order_by('username')

    @permission_classes((IsAdminUser,))
    @authentication_classes((JWTAuthentication,))
    def get(self, request):
        users = [{'id': user.id,
                  'username': user.username,
                  'email': user.email,
                  'links': user.get_absolute_url()} for user in self.queryset.all()]
        return Response(users, status=status.HTTP_200_OK)

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
        serializer = self.serializer_class(data=data,
                                           context={'request': request, 'pk': pk})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

    @authentication_classes((JWTAuthentication,))
    @permission_classes((IsAuthenticatedOnlySelf,))
    def put(self, request, *args, **kwargs):
        self.kwargs.update({'user__id': self.kwargs.get('pk')})
        return self.update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
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


class CompaniesAPIView(APIView):
    queryset = Company.objects.order_by('company_name')

    @permission_classes((IsAuthenticated,))
    @authentication_classes((JWTAuthentication,))
    def get(self, request):
        companies = [{'company_name': company.company_name,
                      'owner': company.owner.username,
                      'administrator': company.administrator.username,
                      'employees': [{'username': employee.username,
                                     'first_name': employee.first_name,
                                     'last_name': employee.last_name,
                                     'middle_name': employee.middle_name,
                                     'position': employee.profile.position,
                                     }
                                    for employee in company.employees.all()],
                      'links': {
                          'self': company.get_absolute_url(),
                          'companies': reverse('api-v1:auth:companies', request=request)}}
                     for company in self.queryset.all()]
        return Response(companies, status=status.HTTP_200_OK)

    @permission_classes((AllowAny,))
    def post(self, request):
        company_name = request.data.get('company_name', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        company = {'company_name': company_name, 'email': email, 'password': password}
        serializer = CompanySerializer(data=company)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            company = Company.objects.get(username=company_name)
            message = f'Company {company.company_name} created.'

            return Response({'message': message}, status=status.HTTP_200_OK)


class CompanyDetailAPIView(APIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    # lookup_field = 'user__id'

    @authentication_classes((JWTAuthentication,))
    @permission_classes((IsAuthenticated,))
    def get(self, request, pk):
        data = {'pk': pk}
        serializer = self.serializer_class(data=data,
                                           context={'request': request, 'pk': pk})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

    @authentication_classes((JWTAuthentication,))
    @permission_classes((IsAuthenticatedOnlySelf,))
    def put(self, request, *args, **kwargs):
        self.kwargs.update({'pk': self.kwargs.get('pk')})
        return self.update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
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

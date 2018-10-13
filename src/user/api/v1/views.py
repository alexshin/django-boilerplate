from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer, MeSerializer, RegisterUserSerializer, EmailConfirmationSerializer, \
    PasswordRecoveryRequestSerializer, PasswordRecoveryConfirmationSerializer

from ...signals import user_password_recovery_requested, user_password_recovery_confirmed

User = get_user_model()


class MeView(RetrieveUpdateAPIView):
    serializer_class = MeSerializer
    http_method_names = ['get', 'put']

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.all()


class RegisterUserView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, format='json', *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailConfirmationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = EmailConfirmationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format='json', *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordRecoveryView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordRecoveryRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format='json', *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        is_valid = serializer.is_valid()
        user_password_recovery_requested.send(sender=self, request=self.request, is_valid=is_valid,
                                              email=serializer.data.get('email'))
        if is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordRecoveryConfirmationView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordRecoveryConfirmationSerializer
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update()
        return context

    def post(self, request, format='json', *args, **kwargs):
        user = self.queryset.get(id=request.data.get('id'))

        serializer = self.serializer_class(user, data=request.data)

        is_valid = serializer.is_valid()
        user_password_recovery_confirmed.send(sender=self, request=self.request, is_valid=is_valid,
                                              code=serializer.validated_data.get('code'))

        if is_valid:
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


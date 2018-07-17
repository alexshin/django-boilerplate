from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import exceptions
import django.contrib.auth.password_validation as password_validators
from rest_framework import serializers, validators

from ...tokens import user_activation_token
from ...signals import user_email_confirmed


User = get_user_model()


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email')


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[validators.UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_password(self, password):
        # validators.validate_password(password=data, user=User)
        # return data

        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(email=self.initial_data.get('email'), password=password)

        errors = {}
        try:
            # validate the password and catch the exception
            password_validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(password)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password')


class EmailConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    code = serializers.CharField(required=True, max_length=255)

    def validate(self, data):
        user_id = data.get('user_id')
        code = data.get('code')

        user = User.objects.filter(id=user_id)

        if not user.exists():
            raise validators.ValidationError('User doesn\'t exist')

        user = user.get()
        if not user.has_perm(perm='user.validate_email', obj=user):
            raise validators.ValidationError('User doesn\'t have permissions to confirm address')

        if not user_activation_token.check_token(user=user, token=code):
            raise validators.ValidationError('Confirmation code is wrong')

        return super().validate(data)

    def create(self, validated_data):
        user = User.objects.get(id=validated_data.get('user_id'))
        user_email_confirmed.send(sender=self, user=user, code=validated_data.get('code'))
        return user

    def update(self, instance, validated_data):
        raise exceptions.PermissionDenied()


class PasswordRecoveryRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        email = self.initial_data.get('email')
        user = User.objects.filter(email=email)

        if not user.exists():
            raise validators.ValidationError('User with current email doesn\'t exist')

        return super().validate(email)

    def create(self, validated_data):
        raise exceptions.PermissionDenied()

    def update(self, instance, validated_data):
        raise exceptions.PermissionDenied()


class PasswordRecoveryConfirmationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=8)
    password_confirmation = serializers.CharField(min_length=8)

    def validate(self, data):
        user_id = data.get('id')
        code = self.initial_data.get('code')
        password = data.get('password')
        password_confirmation = self.initial_data.get('password_confirmation')

        user = User.objects.filter(id=user_id)

        if not user.exists():
            raise validators.ValidationError('User doesn\'t exist')

        if password != password_confirmation:
            raise validators.ValidationError('Passwords do not match')

        user = user.get()
        if not user_activation_token.check_token(user=user, token=code):
            raise validators.ValidationError('Confirmation code is wrong')

        try:
            # validate the password and catch the exception
            password_validators.validate_password(password=password, user=user)
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            raise validators.ValidationError(e.message)

        return super().validate(data)

    def create(self, validated_data):
        raise exceptions.PermissionDenied()

    def save(self, **kwargs):
        self.instance = User.objects.get(pk=self.validated_data.get('id'))
        super().save(**kwargs)

    def update(self, instance, validated_data):
        self.instance.set_password(self.validated_data.get('password'))
        self.instance.save()

        return self.instance

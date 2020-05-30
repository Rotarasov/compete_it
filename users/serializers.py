from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.forms.models import model_to_dict

from rest_framework import serializers

from users.models import User
from events.models import Participation


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    participations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'image', 'participations']


    def get_participations(self, obj):
        participations = Participation.objects.filter(user_id=obj.id)
        return participations.values()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'image', 'password', 'confirm_password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        password2 = attrs.get('confirm_password')

        user = User.objects.filter(email=email).first()

        if user:
            msg = _('Email must be unique.')
            raise serializers.ValidationError(msg)

        if password != password2:
            msg = _('"Password1" and "Password2" must be equal.')
            raise serializers.ValidationError(msg)
        return attrs

    def save(self):
        self.validated_data.pop('confirm_password')
        return User.objects.create_user(**self.validated_data)



class UserChangeSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'image']

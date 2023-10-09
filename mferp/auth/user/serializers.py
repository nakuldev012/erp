import base64

# from django.forms import ValidationError
import requests
from mferp.auth.user.tokens import decode_token, get_access_token
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from mferp.common.errors import ClientErrors, CustomValidationErrorMixin
from .models import MasterConfig, Account
from django.db.models import Q
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from mferp.auth.user.tokens import get_access_token, encode_token
from oauth2_provider.models import AccessToken
from rest_framework import status
from mferp.common.functions import check_password, generate_password


class UserLoginSerializer(CustomValidationErrorMixin, serializers.Serializer):
    """
    Return authenticated user email
    data:
        email and password
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]
        acc_obj = Account.objects.filter(email=data["email"])
        if not acc_obj:
            raise ClientErrors(message="Account Not Found", response_code=404)

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    raise ClientErrors(message="Account deactivate", response_code=401)
            else:
                raise ClientErrors(message="Incorrect Password", response_code=401)
        return data


class SignUpSerializer(CustomValidationErrorMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = "__all__"

    def create(self, validated_data):
        password = generate_password()
        user = Account.objects.create(**validated_data)
        # user.set_password(validated_data["password"])
        user.set_password(password)
        user.save()
        return user


# for bulk user's registration via csv file
class BulkSignUpSerializer(CustomValidationErrorMixin, serializers.Serializer):
    email = serializers.EmailField()
    user_type = serializers.IntegerField()
    first_name = serializers.CharField(max_length=250)
    last_name = serializers.CharField(max_length=250)
    phone_number = serializers.CharField(max_length=17, required=False)

    class Meta:
        model = Account
        fields = "__all__"

    def create(self, validated_data):
        user_type_id = validated_data["user_type"]
        try:
            master_config_instance = MasterConfig.objects.get(id=user_type_id)
        except MasterConfig.DoesNotExist:
            # Handle the case where the MasterConfig instance with the given ID does not exist
            raise serializers.ValidationError("Invalid user_type")
        password = generate_password()
        user = Account.objects.create(
            email=validated_data["email"],
            user_type=master_config_instance,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data["phone_number"],
        )

        return user


class ForgetPasswordEmailSerializer(
    CustomValidationErrorMixin,
    serializers.Serializer,
):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        user = Account.objects.filter(email=data["email"]).last()
        if not user:
            raise ClientErrors(
                message="This email is not registered with us, kindly signup!",
                response_code=404,
            )
        else:
            if user.is_verified:
                if user.is_active:
                    data["user"] = user
                else:
                    raise ClientErrors(message="Account deactivate", response_code=401)
            else:
                raise ClientErrors(
                    message="Account is not verified. Please Verified First! ",
                    response_code=401,
                )
        return data


class VerifyAccountSerializer(CustomValidationErrorMixin, serializers.Serializer):
    q = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        key_code = data.get("q")
        user = decode_token(key_code)
        token = AccessToken.objects.filter(user=user).last().token
        data["user"] = user
        data["token"] = token
        return data


class ResetPasswordEmailSerializer(CustomValidationErrorMixin, serializers.Serializer):
    q = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        key_code = data.get("q", "")
        user = decode_token(key_code)
        data["user"] = user
        return data


# for csv_file
class CsvFileSerializer(CustomValidationErrorMixin, serializers.Serializer):
    path = serializers.CharField()

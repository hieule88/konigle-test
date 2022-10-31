from django.contrib.auth import authenticate
from django.db.models import Q
from django.core.validators import RegexValidator

from rest_framework import serializers

# custom message
from rest_framework.exceptions import APIException
from rest_framework import status

# models
from .models import CustomerEmail, ShopOwner, User

# services
from konigle.services import get_token

# constants
from unity.constants.users import UserValidateType


class MyMessage(APIException):
    """Readers message class"""

    def __init__(self, msg, attrs):
        APIException.__init__(self, msg)
        self.status_code = attrs.get("status_code")
        self.message = msg


# User ================================================================


class CustomerEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerEmail
        fields = "__all__"


class CustomerEmailCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomerEmail
        fields = ("email",)

    def create(self):
        visitor_email_create = CustomerEmail.objects.create(
            shop_owner=self.context.get("request").user.shop_owner,
            email=self.validated_data["email"],
        )
        return visitor_email_create

    def validate_email(self, value):
        if CustomerEmail.objects.filter(
            shop_owner=self.context.get("request").user.shop_owner,
            email=value,
        ).exists():
            raise serializers.ValidationError(
                "A visitor with this email already exists!"
            )
        return value


class AuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def login(self, data):
        msgError = "No active account found with the given credentials."
        try:
            user = authenticate(
                request=self.context.get("request"),
                email=data.get("email"),
                password=data.get("password"),
            )
            data = {"message": "Login successfully!", "result": get_token(user)}
            return data
        except Exception:
            raise MyMessage(
                {"message": msgError}, {"status_code": status.HTTP_400_BAD_REQUEST}
            )


class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOwner
        fields = "__all__"


class ShopOwnerCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=UserValidateType.PASSWORD_REGEX,
                message="Password is invalid",
            )
        ],
    )

    class Meta:
        model = ShopOwner
        fields = (
            "email",
            "password",
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A shop_owner with this email already exists!"
            )
        return value

    def create(self):
        user = User.objects.create(email=self.validated_data["email"])
        user.set_password(self.validated_data["password"])
        user.save()
        # Entry shop_owner
        shop_owner = ShopOwner.objects.create(user=user)
        shop_owner.save()

        return shop_owner

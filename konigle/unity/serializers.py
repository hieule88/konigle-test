from django.contrib.auth import authenticate
from django.db.models import Q
from django.core.validators import RegexValidator

from rest_framework import serializers

# custom message
from rest_framework.exceptions import APIException
from rest_framework import status

# models
from .models import VisitorEmail, Seller, User

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


class VisitorEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorEmail
        fields = "__all__"


class VisitorEmailCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = VisitorEmail
        fields = ("email",)

    def create(self):
        visitor_email_create = VisitorEmail.objects.create(
            seller=self.context.get("request").user.seller,
            email=self.validated_data["email"],
        )
        return visitor_email_create

    def validate_email(self, value):
        if VisitorEmail.objects.filter(
            seller=self.context.get("request").user.seller,
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


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"


class SellerCreateSerializer(serializers.ModelSerializer):
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
        model = Seller
        fields = (
            "email",
            "password",
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A seller with this email already exists!"
            )
        return value

    def create(self):
        user = User.objects.create(email=self.validated_data["email"])
        user.set_password(self.validated_data["password"])
        user.save()
        # Entry seller
        seller = Seller.objects.create(user=user)
        seller.save()

        return seller

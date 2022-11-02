from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework import status

from .models import CustomerEmail, ShopOwner, User

# services
from konigle.services import get_token


PASSWORD_REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class CustomerEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerEmail
        fields = "__all__"


class CustomerEmailAddSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomerEmail
        fields = ("email",)

    def add(self):
        visitor_email_create = CustomerEmail.objects.create(
            shop_owner=self.context.get("request").user.shop_owner,
            email=self.s["email"],
        )
        return visitor_email_create


class AuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def login(self, data):
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
                {"message": "Invalid email or password"}, {"status_code": status.HTTP_400_BAD_REQUEST}
            )


class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOwner
        fields = "__all__"

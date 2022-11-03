from django.contrib.auth import authenticate

from rest_framework import serializers, status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, ShopOwner, CustomerEmail


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]

    def login(self, data):
        try:
            user = authenticate(
                request=self.context.get("request"),
                email=data.get("email"),
                password=data.get("password"),
            )
            data = {"message": "Login successfully!", "result": get_tokens_for_user(user)}
            return data
        except Exception as e:
            raise Response('Invalid Email or Password', status=status.HTTP_400_BAD_REQUEST)


class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOwner
        fields = "__all__"

    def add(self):
        email_added = ShopOwner.objects.create(
            email=self.validated_data["email"],
        )
        return email_added


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
        email_add = CustomerEmail.objects.create(
            shop_owner=self.context.get("request").user.shopowner,
            email=self.validated_data["email"],
        )
        return email_add
from django.shortcuts import render
import datetime
from rest_framework import status, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

from .models import CustomerEmail
from .serializers import (
    UserSerializer,
    ShopOwnerSerializer,
    CustomerEmailSerializer,
    CustomerEmailAddSerializer,
)

# Create your views here.


# Admin Shop Owners see list of all the emails
def index(request):
    emails = CustomerEmail.objects.order_by("-created_date").all()
    count_new_this_month = emails.filter(created_date__month=datetime.date.today().month, created_date__year=datetime.date.today().year).count()
    count_unsubscribed = emails.filter(status=False).count()

    paginator = Paginator(emails, 10)
    page_number = request.GET.get('page')
    page_paginated = paginator.get_page(page_number)

    context = {
        "page_paginated": page_paginated,
        "total_emails": len(emails),
        "amount_new_this_month": count_new_this_month,
        "amount_unsubscribed": count_unsubscribed,
    }
    return render(request, "unity/index.html", context=context)


@api_view(["POST"])
def login_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        result = serializer.login(request.data)
        return Response(result, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        data = {"message": "Logout successfully."}
        return Response(data, status=status.HTTP_200_OK)
    except (AttributeError, ObjectDoesNotExist):
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

class ShopOwnerView(views.APIView):
    def post(self, request):
        serializer = ShopOwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.add()
            data = {"message": "Registered successfully!"}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerEmailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        list_emails = CustomerEmail.objects.filter(shop_owner__user=self.request.user, shop_owner__user__is_active=True)
        if not list_emails:
            return Response(
                {"email": "Not found any email account!"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CustomerEmailSerializer(instance=list_emails, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomerEmailAddSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.add()
            return Response(
                {"message": "Add successfully."}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
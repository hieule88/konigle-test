import email
from venv import create

from django.shortcuts import render, get_object_or_404
import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import CustomerEmail, Seller
from .serializers import (
    CustomerEmailSerializer,
    CustomerEmailCreateSerializer,
    SellerCreateSerializer,
    AuthSerializer,
)

# Create your views here.
import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') 
# function to check if user typed a valid email or not.
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
def is_valid(email):
    if re.fullmatch(regex, email):
        return True
    return False

PAGINATE_BY = 15


#view for user see statistic
def index(request):
    emails = CustomerEmail.objects.all()
    new_this_month = emails.filter(created_date__month=datetime.date.today().month, created_date__year=datetime.date.today().year)
    unsubscribed = emails.filter(status=False)

    paginator = Paginator(emails, PAGINATE_BY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "total_emails": len(emails),
        "amount_new_this_month": len(new_this_month),
        "amount_unsubscribed": len(unsubscribed),
    }
    return render(request, "emails.html", context=context)

@api_view(['POST'])
def get_mail(request):
    """ 
    Validate email.
    If it is a valid email and not exist in database, then save it into database 
    Otherwise, response a error
    """
    data = request.data
    email_name = data["email"]

    if is_valid(email_name):
        if  Email.objects.filter(name = email_name):
            return Response({"message":"already exists"}, status=409)      
        content = data
        email = Email(name=email_name)
        email.save()
        return Response(content,status=201)
    else:
        return Response({"message":"email not valid"}, status=400)

@api_view(["POST"])
def login_view(request):
    serializer = AuthSerializer(data=request.data)
    if serializer.is_valid():
        result = serializer.login(request.data)
        return Response(result, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        data = {"message": "Successfully logged out."}
        return Response(data, status=status.HTTP_200_OK)
    except (AttributeError, ObjectDoesNotExist):
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

class SellerViewSet(viewsets.ModelViewSet):
    serializer_class = SellerCreateSerializer
    permission_classes = []
    pagination_class = None

    def get_queryset(self):
        queryset = Seller.objects.filter(user__is_active=True)
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create()
            data = {"message": "Registered successfully!"}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerEmailViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerEmailSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        queryset = CustomerEmail.objects.filter(
            seller__user=self.request.user, seller__user__is_active=True
        )
        return queryset

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs.get("id"),
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response(
                {"email": "Email not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, id=None):
        try:
            serializer = self.get_serializer(self.get_object())
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"email": "Email not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request, *args, **kwargs):
        serializer = CustomerEmailCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.create()
            return Response(
                {"message": "Create successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

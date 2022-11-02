
from django.conf.urls import include
from django.urls import path

from rest_framework import permissions

from .views import *
                        

# urlpatterns = [
#     path('emails/customer', CustomerEmailView.as_view()),
#     path('emails/shop_owners', ShopOwnerView.as_view()),
#     # auth
#     path('auth/login', login_view),
#     path('auth/logout', logout_view),
# ]
# Define class
email_list = CustomerEmailView.as_view({
    'get': 'get', # Get lists
    'post': 'post' # Create a new
})

seller_list = ShopOwnerView.as_view({
    'post': 'post',
})

urlpatterns = [
    path('emails/customer', email_list),
    path('emails/shop_owners', seller_list),
    # auth
    path('auth/login', login_view),
    path('auth/logout', logout_view),
]

from django.conf.urls import include
from django.urls import path

from rest_framework import permissions

from .views import *
                        

# Define class
email_list = CustomerEmailViewSet.as_view({
    'get': 'list', # Get lists
    'post': 'create' # Create a new
})

email_detail = CustomerEmailViewSet.as_view({
    'get': 'retrieve', # get detail
    # 'patch': 'update', # update
    # 'delete': 'destroy', # delete
})

shop_owner_list = ShopOwnerViewSet.as_view({
    'post': 'create',
})

urlpatterns = [
    path('emails/<int:id>', email_detail, name='email_detail'),
    path('emails', email_list),
    path('shop_owners', shop_owner_list),
    # auth
    path('auth/login', login_view),
    path('auth/logout', logout_view),
]

from django.urls import path

from .views import *
                        

urlpatterns = [
    # get to list all email of logined shop owner
    # post to add a email to logined shop owner
    path('emails/customer', CustomerEmailView.as_view()),
    
    # post to add a shop owner account to the system 
    path('emails/shop_owner', ShopOwnerView.as_view()),
    
    # user login/logout
    path('user/login', login_view),
    path('user/logout', logout_view),
]
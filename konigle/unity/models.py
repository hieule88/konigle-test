from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
# Create your models here.


class User(AbstractUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    

class ShopOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.email


class CustomerEmail(models.Model):
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    status = models.BooleanField(default=True,blank=True,null=True)
    created_date = models.DateTimeField(auto_now=True,  null=False, blank=False)

    def __str__(self):
        return self.email
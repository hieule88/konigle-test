from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
# Create your models here.


class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ShopOwner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
        
    def __str__(self):
        return self.user.email


class CustomerEmail(models.Model):
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE)
    email = models.EmailField(max_length=256)
    status = models.BooleanField(default=True, blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True, null=False, blank=False)
        
    def __str__(self) -> str:
        return f"{self.email}"
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser
from django.utils import timezone

from .manager import CustomUserManager
# Create your models here.


# class User(AbstractUser, PermissionsMixin):
#     def __str__(self):
#         return self.email
class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(('first name'), max_length=30)
    last_name = models.CharField(('last name'), max_length=150)
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.\
                                              Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ShopOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ('-pk',)
        
    def __str__(self):
        return self.user.email


class CustomerEmail(models.Model):
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    status = models.BooleanField(default=True,blank=True,null=True)
    created_date = models.DateTimeField(auto_now=True,  null=False, blank=False)

    class Meta:
        ordering = ('-pk',)
        
    def __str__(self):
        return self.email
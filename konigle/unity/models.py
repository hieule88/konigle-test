from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .manager import CustomUserManager
from .constants.visitor_emails import VisitorEmailStatusType, VisitorEmailIsSentType
# Create your models here.
# class Email(AbstractBaseUser, PermissionsMixin):
#     name = models.EmailField(max_length=256, unique=True)
#     date = models.DateTimeField(auto_now=True,  null=False, blank=False)
#     status = models.BooleanField(default=True,blank=True,null=True)

#     USERNAME_FIELD = 'name'
    
#     def __str__(self) -> str:
#         return f"{self.name} {self.date}"

# extend User system table
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
    
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_email_sent = models.IntegerField(default=VisitorEmailIsSentType.UNSENT)
    #
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ('-pk',)
        db_table = 'sellers'
    
    def __str__(self):
        return self.user.email
    
    def get_user_email(self):
        try:
            return self.user.email
        except:
            return None
    
class VisitorEmail(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    status = models.IntegerField(default=VisitorEmailStatusType.SUBSCRIBED)
    #
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ('-pk',)
        db_table = 'visitor_emails'

    def __str__(self):
        return self.email